#!/usr/bin/python

import json
import os
import re
import datetime
import uuid

from flask import Flask, request, jsonify
from sqlalchemy.inspection import inspect
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc, update, and_

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)
# Setup Bcrypt
bcrypt = Bcrypt(app)
# Setup SQLAlchemy app config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{pwd}@{host}/{db}'.format(
    user=os.getenv('MYSQL_USER', 'root'),
    pwd=os.getenv('MYSQL_PASSWORD', ''),
    host=os.getenv('MYSQL_HOST', 'localhost'),
    db=os.getenv('MYSQL_DATABASE', '')
)
# Setup SQLAlchemy
db = SQLAlchemy(app)

# Setup Flask-Marshmallow
ma = Marshmallow(app)

# DB Models
class Diary(db.Model):
    entry_id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(db.Integer(), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    entry_title = db.Column(db.String())
    entry_text = db.Column(db.String())
    entry_is_public = db.Column(db.Boolean, nullable=False)



class DiarySchema(ma.ModelSchema):
    class Meta:
        model = Diary
        fields = ('entry_id', 'entry_title', 'author_id', 'entry_date', 'entry_is_public', 'entry_text')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sign_in_count = db.Column(db.Integer, nullable=False)
    locked_at = db.Column(db.DateTime)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    session_created_at = db.Column(db.DateTime)

    def new_failed_login(self):
        # Reset lock if lock is expired
        if self.locked_at is not None:
            self.sign_in_count = 0
            self.locked_at = None

        # Increment failed attempts and set lock
        self.sign_in_count += 1
        if self.sign_in_count >= 3:
            self.locked_at = datetime.datetime.now()

    def is_locked(self):
        if self.locked_at is None:
            return False

        lock_expire_at = self.locked_at + datetime.timedelta(hours=1)
        return lock_expire_at >= datetime.datetime.now()

    def new_session(self, reset=False):
        self.sign_in_count = 0,
        self.locked_at = None

        self.session_token = str(uuid.uuid4()),
        if reset:
            self.session_created_at = None
        else:
            self.session_created_at = datetime.datetime.now()

    def in_valid_session(self):
        if self.session_created_at is None or self.is_locked():
            return False
        expire_at = self.session_created_at + datetime.timedelta(hours=3)
        return expire_at >= datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % self.username


def get_user(session_token):
    """Authenticate a user by session_token"""

    user = User.query.filter_by(session_token=session_token).first()
    if user is None:
        return None
    elif user.in_valid_session():
        return user
    else:
        return None


ENDPOINT_LIST = [
    '/',
    '/meta/heartbeat',
    '/meta/members',
    '/users/register',
    '/users/authenticate',
    '/users/expire',
    '/users',
    '/diary/permission',
    '/diary/delete',
    '/diary/create',
    '/diary'
]


def make_json_response(data, root=None, status=True, code=200):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if root is not None:
        to_serialize = root

    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
    else:
        to_serialize['status'] = False
        if data is not None:
            to_serialize['error'] = data

    return app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json')


@app.route("/")
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)


@app.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@app.route("/meta/members")
def meta_members():
    """Returns a list of team members"""
    with open("./team_members.txt") as f:
        team_members = f.read().strip().split("\n")
    return make_json_response(team_members)


@app.route("/users/register", methods=["POST"])
def user_register():
    """Create a user account"""

    body = request.get_json(silent=True) or {}
    username = str(body.get('username') or '')
    password = str(body.get('password') or '')
    fullname = str(body.get('fullname') or '')
    age = body.get('age') or 0

    errors = []
    if len(username) == 0:
        errors.append("Username cannot be empty")

    if len(password) == 0:
        errors.append("Password cannot be empty")
    elif re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                  password) is None:
        errors.append("Password must have minimum eight characters, " +
                      "at least one uppercase letter, one lowercase letter " +
                      "and one number")

    if len(fullname) == 0:
        errors.append("Fullname cannot be empty")

    if not isinstance(age, int):
        errors.append("Age must be an integer and cannot be empty")
    elif age <= 0 or age > 199:
        errors.append("Age must be within 1~199")

    if len(errors) > 0:
        return make_json_response(errors[0], status=False)

    user = User(
        username=username,
        encrypted_password=bcrypt.generate_password_hash(password),
        fullname=fullname,
        age=age)

    try:
        user.new_session(reset=True)
        db.session.add(user)
        db.session.commit()

        return make_json_response(None, status=True, code=201)
    except exc.IntegrityError as err:
        return make_json_response("User already exists", status=False)
    except exc.SQLAlchemyError as err:
        return make_json_response("Please try again later", status=False)


@app.route("/users/authenticate", methods=["POST"])
def user_authenticate():
    """Authenticate a user by password and return a token"""

    body = request.get_json(silent=True) or {}
    username = str(body.get('username') or '')
    password = str(body.get('password') or '')

    if len(username) == 0 or len(password) == 0:
        return make_json_response("Username/Password cannot be empty",
                                  status=False)

    notFoundErr = "Username/Password not found"

    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_json_response(notFoundErr, status=False)
    elif user.is_locked():
        return make_json_response(notFoundErr, status=False)

    if bcrypt.check_password_hash(user.encrypted_password, password):
        try:
            user.new_session()
            db.session.add(user)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            app.logger.info(err)
            return make_json_response(notFoundErr, status=False)

        return make_json_response(None, root={'token': user.session_token})

    try:
        user.new_failed_login()
        db.session.add(user)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        app.logger.info(err)

    return make_json_response(notFoundErr, status=False)


@app.route("/users/expire", methods=["POST"])
def user_expire():
    """Expire an authenticated token"""

    body = request.get_json(silent=True) or {}
    token = str(body.get('token') or '')

    user = get_user(token)
    if user is None:
        return make_json_response(None, status=False)

    try:
        user.new_session(reset=True)
        db.session.add(user)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        app.logger.info(err)
        return make_json_response(None, status=False)

    return make_json_response(None)


@app.route("/users", methods=["POST"])
def users():
    """Retrieve user information"""

    body = request.get_json(silent=True) or {}
    token = str(body.get('token') or '')

    user = get_user(token)
    if user is None:
        return make_json_response(None, status=False)

    return make_json_response(None, root={
        "username": user.username,
        "fullname": user.fullname,
        "age": user.age
    })


@app.route("/diary", methods=["GET", "POST"])
def diary_retrieve():
    """Retrieve user (POST) or public (GET) diary entries"""

    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        token = str(body.get('token') or '')
        authorNotFoundErr = "Invalid authentication token."

        author = get_user(token)
        if author is None:
            return make_json_response(authorNotFoundErr, status=False)

        diary_schema = DiarySchema(many=True)
        entry_list = Diary.query.filter_by(author_id=author.id).order_by(Diary.entry_id).all()
        result = diary_schema.dump(entry_list)
        return jsonify(result), 200

    else:
        cols = ['entry_id', 'entry_title', 'author_id', 'entry_date', 'entry_is_public', 'entry_text']
        data = Diary.query.filter_by(entry_is_public=True).order_by(Diary.entry_id).all()
        result = [{col: getattr(d, col) for col in cols} for d in data]
        return jsonify(result=result)


@app.route("/diary/create", methods=["POST"])
def diary_create_entry():
    """Create a new diary entry"""

    body = request.get_json(silent=True) or {}
    token = str(body.get('token') or '')
    title = str(body.get('title') or '')
    is_public = body.get('public')
    text = str(body.get('text') or '')
    authorNotFoundErr = "Invalid authentication token."

    author = get_user(token)
    if author is None:
        return make_json_response(authorNotFoundErr, status=False)

    diary = Diary(
        entry_date=datetime.datetime.now(),
        entry_title=title,
        entry_text=text,
        entry_is_public=is_public,
        author_id=author.id)
        
    try:
        db.session.add(diary)
        db.session.commit()
        return make_json_response(None, status=True, root={
            "result":diary.entry_id
        })
    except exc.IntegrityError as err:
        return make_json_response("Something wrong with data", status=False)
    except exc.SQLAlchemyError as err:
        return make_json_response("Please try again later", status=False)


@app.route("/diary/delete", methods=["POST"])
def diary_delete_entry():
    """Deletes a diary entry"""

    body = request.get_json(silent=True) or {}
    token = str(body.get('token') or '')
    entry_id = str(body.get('id') or '')
    authorNotFoundErr = "Invalid authentication token."

    author = get_user(token)
    if author is None:
        return make_json_response(authorNotFoundErr, status=False)

    entry = Diary.query.filter((Diary.entry_id==entry_id) & (Diary.author_id==author.id)).first()

    try:
        db.session.delete(entry)
        db.session.commit()
        return make_json_response(None, status=True)
    except exc.IntegrityError as err:
        return make_json_response("Something wrong with data", status=False)
    except exc.SQLAlchemyError as err:
        return make_json_response("Entry does not exist, or you do not have permission to delete this entry.", status=False)


@app.route("/diary/permission", methods=["POST"])
def diary_change_permission():
    """Updates a diary entry permission"""

    body = request.get_json(silent=True) or {}
    token = str(body.get('token') or '')
    entry_id = str(body.get('id') or '')
    is_public = body.get('public')
    authorNotFoundErr = "Invalid authentication token."

    author = get_user(token)
    if author is None:
        return make_json_response(authorNotFoundErr, status=False)

    entry_count = Diary.query.filter((Diary.entry_id==entry_id) & (Diary.author_id==author.id)).count()

    if (entry_count == 0) or (entry_count > 1):
        return make_json_response("Entry does not exist, or you do not have permission to modify this entry.", status=False)

    entry = Diary.query.filter((Diary.entry_id==entry_id) & (Diary.author_id==author.id)).update({Diary.entry_is_public: is_public})

    try:
        db.session.commit()
        return make_json_response(None, status=True)
    except exc.IntegrityError as err:
        return make_json_response("Something wrong with data", status=False)
    except exc.SQLAlchemyError as err:
        return make_json_response("Please try again later", status=False)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")

#!/usr/bin/python

import json
import os
import re
import datetime
import uuid

from flask import Flask, request

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

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

# DB Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sign_in_count = db.Column(db.Integer, nullable=False)
    locked_at = db.Column(db.DateTime)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    session_created_at = db.Column(db.DateTime, nullable=False)

    def is_locked(self):
        return self.locked_at is not None

    def is_session_token_expired(self):
        expire_at = self.session_created_at + datetime.timedelta(hours=3)
        return expire_at >= datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % self.username


def authenticate(session_token):
    """Authenticate a user by session_token"""

    user = User.query.filter_by(session_token=session_token).first()
    if user is None:
        return None
    elif user.is_session_token_expired():
        return None
    else:
        return user


# Remember to update this list
ENDPOINT_LIST = [
    '/',
    '/meta/heartbeat',
    '/meta/members',
    '/users/register'
]


def make_json_response(data, status=True, code=200):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
    else:
        to_serialize['status'] = False
        to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json')
    return response


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

    body = request.get_json()

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
        return make_json_response(errors, status=False)

    user = User(
        username=username,
        encrypted_password=bcrypt.generate_password_hash(password),
        fullname=fullname,
        age=age,
        sign_in_count=0,
        session_token=str(uuid.uuid4()),
        session_created_at=datetime.datetime.now()
    )

    try:
        db.session.add(user)
        db.session.commit()

        return make_json_response(None, status=True, code=201)
    except exc.IntegrityError as err:
        print(err)
        return make_json_response(["Username is duplicated"], status=False)
    except exc.SQLAlchemyError as err:
        print(err)
        return make_json_response(["Please try again later"], status=False)


@app.route("/users")
def users():
    """List all user accounts"""

    users = User.query.all()
    if len(users) == 0:
        return make_json_response(None)
    else:
        return make_json_response([user.username for user in users])


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")

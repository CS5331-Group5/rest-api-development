#!/usr/bin/python

import json
import os

from flask import Flask, request

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)
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

    def __repr__(self):
        return '<User %r>' % self.username

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members']

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
    user = User(username="Hello")
    db.session.add(user)
    db.session.commit()
    return make_json_response(user.id)


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

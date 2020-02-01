from flask import Flask
from flask_cors import CORS
from models import db, User
from flask_jwt import JWT
from config import config
from routes.user import user_api
from init_db import initialize_superuser, initialize_subjects

# instantiate the app
app = Flask(__name__)
app.register_blueprint(user_api, url_prefix='/user')

# configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = config['SECRET_KEY']

db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def authenticate(username, password):
    user = User.get_by_username(username)
    if user and user.check_hash(password):
        return user


def identity(payload):
    username = payload['identity']
    return User.get_by_username(username)


jwt = JWT(app, authenticate, identity)

@app.before_first_request
def initialize_database():
    initialize_subjects()
    initialize_superuser()

if __name__ == '__main__':
    app.run()

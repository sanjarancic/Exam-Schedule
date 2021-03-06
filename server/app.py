from flask import Flask
from flask_cors import CORS
from models import db, User
from flask_jwt import JWT
from config import config
from routes.user import user_api
from routes.exam import exam_api
from init_db import initialize_superuser, initialize_subjects
import datetime

# instantiate the app
app = Flask(__name__)
app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(exam_api)

# configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = config['SECRET_KEY']

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=365)

db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def authenticate(username, password):
    user = User.get_by_username(username)
    if user and user.check_hash(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)



jwt = JWT(app, authenticate, identity)

@app.before_first_request
def initialize_database():
    # db.create_all()
    initialize_subjects()
    initialize_superuser()

if __name__ == '__main__':
    app.run()

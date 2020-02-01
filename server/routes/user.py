from models import User
from flask import request, Blueprint, jsonify
from utils import custom_response
from flask_jwt import jwt_required, current_identity


user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']

    user = User.get_by_username(username)

    if user:
        message = {'error': 'User already exist, please try again'}
        return custom_response(message, 400)

    user = User(username, password)
    user.save()
    return custom_response({'message': 'Successfully registered'}, 201)


@user_api.route('/current', methods=['POST'])
@jwt_required()
def protected():
    current_user = current_identity
    print('Current user is {}'.format(current_user.serialize()))
    return custom_response({'user': current_user.serialize()})
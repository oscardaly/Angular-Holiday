from flask import Blueprint, jsonify, make_response, request
import jwt
import datetime
from login import utils

login_blueprint = Blueprint('login', __name__)
BASE_URL = "/api/v1.0"
# staff = db.staff
# blacklist = db.blacklist


@login_blueprint.route(BASE_URL + "/login", methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 
                            'exp' : datetime.datetime.utcnow() + \
                                    datetime.timedelta(minutes=120)}, 
                            'SECRET_KEY')
        return jsonify({'token' : token.decode('UTF-8')})
    
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})


@login_blueprint.route(BASE_URL + "/logout", methods=['GET'])
@utils.check_for_jwt
def logout():
    token = request.headers['x-access-token']
    # blacklist.insert_one({"token":token})
    return make_response(jsonify({'message' : 'Logout successful'}), 200)
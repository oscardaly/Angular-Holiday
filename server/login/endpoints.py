from flask import Blueprint, jsonify, make_response, request
import jwt
import datetime

login_blueprint = Blueprint('login', __name__)

users =  {
    "user" : {
        "name" : "user",
        "password" : "user",
        "profile_picture" : "",
        "type" : "user"
    }
}

BASE_URL = "/api/v1.0/login"


@login_blueprint.route(BASE_URL, methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 
                            'exp' : datetime.datetime.utcnow() + \
                                    datetime.timedelta(minutes=30)}, 
                            'SECRET_KEY')
        return jsonify({'token' : token.decode('UTF-8')})
    
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})


# log out - remove token?
from flask import Blueprint, jsonify, make_response, request
import jwt
import os
import datetime
from login import utils
from pymongo import MongoClient
import bcrypt
from setup_mongodb import helpers
from dotenv import load_dotenv

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.holidayDB
usersDB = db.users
blacklistDB = db.blacklist

login_blueprint = Blueprint('login', __name__)
BASE_URL = "/api/v1.0"
load_dotenv()

@login_blueprint.route(BASE_URL + "/login", methods=['GET'])
def login():
    auth = request.authorization
    if auth:
        user = usersDB.find_one({'username' : auth.username })

        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user["password"]):
                token = jwt.encode(
                    {
                        'username' : auth.username,
                        'admin' : user["admin"], 
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                    }, os.environ["SECRET_KEY"])
                os.environ["CURRENT_USER"] = auth.username
                return make_response(jsonify({'token':token.decode('UTF-8')}), 200)

            else:
                return make_response(jsonify({'message' : 'Incorrect password'}), 401)
                
        else:
            return make_response(jsonify({'message' : 'Incorrect username'}), 401) 
    
    else:
        return make_response({'message' : 'Authentication required'}, 401)


@login_blueprint.route(BASE_URL + "/logout", methods=['GET'])
@utils.check_for_jwt
def logout():
    print("1")
    try:
        token = request.headers['x-access-token']

        if token is not None:
            blacklistDB.insert_one({
                "timestamp" : datetime.datetime.now(tz=datetime.timezone.utc),
                "token" : token
            })
            os.environ["CURRENT_USER"] = ""
            return make_response(jsonify({'message' : 'Logout successful'}), 200)
        
        else:
            return make_response(jsonify({'error' : 'No token found'}), 404)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)
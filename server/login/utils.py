from flask import make_response, jsonify, request
import jwt
import os
from functools import wraps
from dotenv import load_dotenv
from setup_mongodb import config, helpers

load_dotenv()


def check_for_jwt(function):
    @wraps(function)
    def check_for_jwt_wrapper(*args, **kwargs):
        token = None
        print("1")
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print(token)
            try:
                blacklisted_token = config.blacklist.find_one({"token" : token})

                if blacklisted_token is not None:
                    return make_response(jsonify({'message' : 'Token has been cancelled'}), 401)
                
                data = jwt.decode(token, os.environ["SECRET_KEY"])
        
            except:
                return jsonify({'message' : 'Token is invalid'}), 401

        else:
            return jsonify({'message' : 'Token is missing'}), 401

        return function(*args, **kwargs)
    return check_for_jwt_wrapper


def admin_or_account_owner_required(function):
    @wraps(function)
    def admin_required_wrapper(username):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
            try:
                blacklisted_token = config.blacklist.find_one({"token" : token})

                if blacklisted_token is not None:
                    return make_response(jsonify({'message' : 'Token has been cancelled'}), 401)

                data = jwt.decode(token, os.environ["SECRET_KEY"])

                if data["admin"] or data["username"] == username:
                    return function(username)
            
                else:
                    return make_response(jsonify({'message' : 'Admin access required'}), 401)
                
            except:
                return jsonify({'message' : 'Token is invalid'}), 401

        else:
            return jsonify({'message' : 'Token is missing'}), 401
            
    return admin_required_wrapper


def admin_or_post_owner_required(function):
    @wraps(function)
    def admin_required_wrapper(id):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
            try:
                blacklisted_token = config.blacklist.find_one({"token" : token})

                if blacklisted_token is not None:
                    return make_response(jsonify({'message' : 'Token has been cancelled'}), 401)
                
                data = jwt.decode(token, os.environ["SECRET_KEY"])
                post = helpers.get_post_by_id(config.posts, id)

                if data["admin"] or data["username"] == post["author"]["username"]:
                    return function(id)
            
                else:
                    return make_response(jsonify({'message' : 'Admin access required'}), 401)
                
            except:
                return jsonify({'message' : 'Token is invalid'}), 401

        else:
            return jsonify({'message' : 'Token is missing'}), 401
            
    return admin_required_wrapper


def admin_or_comment_owner_required(function):
    @wraps(function)
    def admin_required_wrapper(comment_id):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
            try:
                blacklisted_token = config.blacklist.find_one({"token" : token})

                if blacklisted_token is not None:
                    return make_response(jsonify({'message' : 'Token has been cancelled'}), 401)
                
                data = jwt.decode(token, os.environ["SECRET_KEY"])
                comment = helpers.get_post_comment_by_id(config.posts, comment_id)

                if data["admin"] or data["username"] == comment["username"]:
                    return function(comment_id)
            
                else:
                    return make_response(jsonify({'message' : 'Admin access required'}), 401)
                
            except:
                return jsonify({'message' : 'Token is invalid'}), 401

        else:
            return jsonify({'message' : 'Token is missing'}), 401
            
    return admin_required_wrapper

def admin_or_comment_owner_required_for_delete(function):
    @wraps(function)
    def admin_required_wrapper(post_id, comment_id):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
            try:
                blacklisted_token = config.blacklist.find_one({"token" : token})

                if blacklisted_token is not None:
                    return make_response(jsonify({'message' : 'Token has been cancelled'}), 401)
                
                data = jwt.decode(token, os.environ["SECRET_KEY"])
                comment = helpers.get_post_comment_by_id(config.posts, comment_id)

                if data["admin"] or data["username"] == comment["username"]:
                    return function(post_id, comment_id)
            
                else:
                    return make_response(jsonify({'message' : 'Admin access required'}), 401)
                
            except:
                return jsonify({'message' : 'Token is invalid'}), 401

        else:
            return jsonify({'message' : 'Token is missing'}), 401
            
    return admin_required_wrapper
from flask import Flask, jsonify, request
import jwt
from functools import wraps
from ..app import app

def check_for_jwt(function):
    @wraps(function)
    def check_for_jwt_wrapper(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing'}), 401
            
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        
        except:
            return jsonify({'message' : 'Token is invalid'}), 401

        return function(*args, **kwargs)
    return check_for_jwt_wrapper
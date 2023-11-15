from flask import Blueprint, jsonify, make_response, request
from login.utils import check_for_jwt
# from app import BASE_URL

users_blueprint = Blueprint('users', __name__)

# BASE_URL = BASE_URL + "/users"
BASE_URL = "/api/v1.0/users"


users =  {
    "user" : {
        "name" : "user",
        "password" : "user",
        "profile_picture" : "",
        "type" : "user"
    },
    "admin" : {
        "name" : "admin",
        "password" : "admin",
        "profile_picture" : "",
        "type" : "admin"       
    },
    "dummy" : {
        "name" : "dummy",
        "password" : "dummy",
        "profile_picture" : "",
        "type" : "user"       
    }
}


@users_blueprint.route(BASE_URL, methods=["GET"])
def get_all_users():
    return make_response( jsonify( users ), 200 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["GET"])
@check_for_jwt
def get_user_by_username(username):
    return make_response( jsonify(  users[username] ), 200 )


@users_blueprint.route(BASE_URL, methods=["POST"])
def add_user():
        # check for same id/username in backend
        username = request.form["username"]
        new_user = { 
                "name" : request.form["name"],
                "password" : request.form["password"],
                "profile_picture" : request.form["profile_picture"],
                "type" : "user"
        }
        
        users[username] = new_user
        return make_response( jsonify( { username : new_user } ), 201 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["PUT"])
@check_for_jwt
def edit_user(username):
    users[username]["name"] = request.form["name"]
    users[username]["password"] = request.form["password"]
    users[username]["profile_picture"] = request.form["profile_picture"]
    return make_response( jsonify( { username : users[username] } ), 200 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["DELETE"])
@check_for_jwt
def delete_user(username):
    del users[username]
    return make_response( jsonify( {} ), 200)
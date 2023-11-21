from flask import Blueprint, jsonify, make_response, request
from login import utils
from setup_mongodb import config, helpers
import bcrypt

users_blueprint = Blueprint('users', __name__)
BASE_URL = "/api/v1.0/users"


@users_blueprint.route(BASE_URL, methods=["GET"])
def get_all_users():
    users = helpers.get_users_from_mongo(config.users)
    return make_response( jsonify( users ), 200 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["GET"])
# @utils.check_for_jwt
@utils.admin_or_account_owner_required
def get_user_by_username(username):
    user = helpers.get_user_from_mongo_by_username(config.users, username)
    
    if user is not None:
        return make_response( jsonify(  user ), 200 )

    else:
        return make_response(jsonify({ "error" : "User not found" }), 404)


@users_blueprint.route(BASE_URL, methods=["POST"])
def add_user():
    try:
        user = helpers.get_user_from_mongo_by_username(config.users, request.json["username"])

        if user is None:
            hashed_password = bcrypt.hashpw(request.json["password"].encode('utf-8'), bcrypt.gensalt())
            new_user = { 
                    "username" : request.json["username"],
                    "forename" : request.json["forename"],
                    "surname" : request.json["surname"],
                    "password" : hashed_password,
                    "profile_picture" : request.json["profile_picture"],
                    "admin" : False
            }

            new_user_id = config.users.insert_one(new_user)
            new_user_link = "http://localhost:5000" + BASE_URL + str(new_user_id.inserted_id)

            return make_response( jsonify( { "url" : new_user_link } ), 201 )

        else:
            return make_response(jsonify({ "error" : "Username already exists" }), 409)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)



@users_blueprint.route(BASE_URL + "/<string:username>", methods=["PUT"])
# @utils.check_for_jwt
@utils.admin_or_account_owner_required
def edit_user(username):
    try:
        hashed_password = bcrypt.hashpw(request.json["password"].encode('utf-8'), bcrypt.gensalt())
        response = config.users.update_one({ "username" : username }, 
        {
            "$set" : 
                { 
                    "forename" : request.json["forename"],
                    "surname" : request.json["surname"],
                    "password" : hashed_password,
                    "profile_picture" : request.json["profile_picture"],
                    "username" : request.json["username"],
                }
        })

        if response.matched_count == 1:
            edited_user_link = "http://localhost:5000" + BASE_URL + "/" + username
            return make_response( jsonify({ "url" : edited_user_link } ), 200)
        
        else:
            return make_response(jsonify( { "error" : "User not found" } ), 404)
    
    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["DELETE"])
# @utils.check_for_jwt
@utils.admin_or_account_owner_required
def delete_user(username):
    result = config.users.delete_one( { "username" : username } )
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 200)

    else:
        return make_response(jsonify( { "error" : "User not found" } ), 404)
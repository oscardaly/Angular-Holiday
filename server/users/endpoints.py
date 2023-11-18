from flask import Blueprint, jsonify, make_response, request
from login import utils
from setup_mongodb import config, helpers

users_blueprint = Blueprint('users', __name__)
BASE_URL = "/api/v1.0/users"


@users_blueprint.route(BASE_URL, methods=["GET"])
def get_all_users():
    users = helpers.get_users_from_mongo(config.users)
    return make_response( jsonify( users ), 200 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["GET"])
@utils.check_for_jwt
def get_user_by_username(username):
    user = helpers.get_user_from_mongo_by_username(config.users, username)
    
    if user is not None:
        return make_response( jsonify(  user ), 200 )

    else:
        return make_response(jsonify({ "error" : "User not found" }), 404)


@users_blueprint.route(BASE_URL, methods=["POST"])
def add_user():
    try:
        user = helpers.get_user_from_mongo_by_username(config.users, request.form["username"])
    
        if user is None:
            new_user = { 
                    "username" : request.form["username"],
                    "forename" : request.form["forename"],
                    "surname" : request.form["surname"],
                    "password" : request.form["password"],
                    "profile_picture" : request.form["profile_picture"],
                    "type" : "user"
            }
            
            new_user_id = config.users.insert_one(new_user)
            new_user_link = "http://localhost:5000" + BASE_URL + str(new_user_id.inserted_id)

            return make_response( jsonify( { "url" : new_user_link } ), 201 )

        else:
            return make_response(jsonify({ "error" : "Username already exists" }), 409)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)



@users_blueprint.route(BASE_URL + "/<string:username>", methods=["PUT"])
@utils.check_for_jwt
def edit_user(username):
    try:
        response = config.users.update_one({ "username" : username }, 
        {
            "$set" : 
                { 
                    "forename" : request.form["forename"],
                    "surname" : request.form["surname"],
                    "password" : request.form["password"],
                    "profile_picture" : request.form["profile_picture"],
                    "username" : request.form["username"]
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
@utils.check_for_jwt
def delete_user(username):
    result = config.users.delete_one( { "username" : username } )
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 200)

    else:
        return make_response(jsonify( { "error" : "User not found" } ), 404)
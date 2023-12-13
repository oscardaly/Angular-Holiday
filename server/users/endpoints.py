import datetime
from flask import Blueprint, jsonify, make_response, request
from login import utils
from setup_mongodb import config, helpers
import bcrypt
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

users_blueprint = Blueprint('users', __name__)
BASE_URL = "/api/v1.0/users"


@users_blueprint.route(BASE_URL, methods=["GET"])
def get_all_users():
    users = helpers.get_users_from_mongo(config.users)
    return make_response( jsonify( users ), 200 )


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["GET"])
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
        request_data = request.get_json(force=True)
        user = helpers.get_user_from_mongo_by_username(config.users, request_data["username"])
        
        if (request_data["username"] != "" and request_data["forename"] != "" and 
            request_data["surname"] != "" and request_data["password"] != "" and request_data["profile_picture"] != ""):
            if user is None:
                hashed_password = bcrypt.hashpw(request_data["password"].encode('utf-8'), bcrypt.gensalt())
                new_user = { 
                        "username" : request_data["username"],
                        "forename" : request_data["forename"],
                        "surname" : request_data["surname"],
                        "password" : hashed_password,
                        "profile_picture" : request_data["profile_picture"],
                        "admin" : False
                }

                new_user_id = config.users.insert_one(new_user)
                new_user_link = "http://localhost:5000" + BASE_URL + "/" + str(new_user_id.inserted_id)

                return make_response( jsonify( { "url" : new_user_link } ), 201 )

            else:
                return make_response(jsonify({ "error" : "Username already exists" }), 409)
        
        else:
           return make_response(jsonify( { "error" : "Missing form data" } ), 404)         

    except:
        return make_response(jsonify( { "error" : "Server error" } ), 500)



@users_blueprint.route(BASE_URL + "/<string:username>", methods=["PUT"])
@utils.admin_or_account_owner_required
def edit_user(username):
    try:
        hashed_password = bcrypt.hashpw(request.json["password"].encode('utf-8'), bcrypt.gensalt())
        updated_user_details = { 
            "forename" : request.json["forename"],
            "surname" : request.json["surname"],
            "password" : hashed_password,
            "profile_picture" : request.json["profile_picture"],
            "username" : request.json["username"]
        }

        response = config.users.update_one({ "username" : username }, { "$set" : updated_user_details })
        os.environ["CURRENT_USER"] = request.json["username"]

        if response.matched_count == 1:
            del updated_user_details["password"]
            config.posts.update_many({ "author.username" : username}, { "$set" : { "author" : updated_user_details }})
            
            updated_user_details = helpers.update_user_object_for_comment_subdocument(updated_user_details)
            config.posts.update_many({ "comments" : { "$elemMatch" : { "username" : username }}}, { "$set" : updated_user_details })

            edited_user_link = "http://localhost:5000" + BASE_URL + "/" + request.json["username"]
            return make_response( jsonify({ "url" : edited_user_link } ), 200)
        
        else:
            return make_response(jsonify( { "error" : "User not found" } ), 404)
    
    except Exception as error:
        return make_response(jsonify( { "error" : traceback.print_exc() } ), 404)


@users_blueprint.route(BASE_URL + "/<string:username>", methods=["DELETE"])
@utils.admin_or_account_owner_required
def delete_user(username):
    token = request.headers['x-access-token']
    
    if token is not None:
        config.blacklist.insert_one({
            "timestamp" : datetime.datetime.now(tz=datetime.timezone.utc),
            "token" : token
            })

    result = config.users.delete_one( { "username" : username } ) 

    if result.deleted_count == 1:
        config.posts.delete_many({ "author.username" : username})
        config.posts.update_many( { }, { "$pull" : { "comments" : { "username" : username } } } ) 
        os.environ["CURRENT_USER"] = ""
        return make_response( jsonify( {} ), 200)

    else:
        return make_response(jsonify( { "error" : "User not found" } ), 404)
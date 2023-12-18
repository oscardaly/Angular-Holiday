from login import utils
from flask import Blueprint, jsonify, make_response, request
from setup_mongodb import config, helpers
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

posts_blueprint = Blueprint('posts', __name__)
BASE_URL = "/api/v1.0/posts"


@posts_blueprint.route(BASE_URL, methods=["GET"])
def get_all_posts():
    page_num, page_size = 1, 10
    sort_by_direction = 1
    sort_by_function = "_id"
    title = None
    city = None
    country = None

    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    if request.args.get('sort_by_direction'):
        sort_by_direction = int(request.args.get('sort_by_direction'))
    
    if request.args.get('sort_by_function'):
        sort_by_function = request.args.get('sort_by_function')
 
    if request.args.get('title'):
        title = request.args.get('title')

    if request.args.get('country'):
        country = request.args.get('country')
    
    if request.args.get('city'):
        city = request.args.get('city') 
    
    page_start = (page_size * (page_num - 1))
    data_to_return = helpers.get_posts_from_mongo(config.posts, page_size, page_start, sort_by_direction, sort_by_function, title, country, city)
    return make_response(jsonify( data_to_return ), 200)


@posts_blueprint.route(BASE_URL + "/get-post", methods=["GET"])
def get_post():
    post = None

    if request.args.get('id'):
        post = helpers.get_post_by_id(config.posts, request.args.get('id'))
    
    elif request.args.get('title'):
        post = helpers.get_post_by_title(config.posts, request.args.get('title'))

    if post is not None:
        return make_response(jsonify(post), 200)

    else:
        return make_response(jsonify({ "error" : "Post not found" }), 404)


@posts_blueprint.route(BASE_URL, methods=["POST"])
@utils.check_for_jwt
def add_post():
    try:
        data = request.get_json()
        post = helpers.get_post_by_title(config.posts, data["title"])
        
        if post is None:
            city_for_post = helpers.get_city_by_id(config.cities, data["cityID"])

            if city_for_post:
                current_user = helpers.get_user_from_mongo_by_username(config.users, os.environ["CURRENT_USER"])
                new_post = {
                    "title" : data["title"],
                    "author" : {
                        "username" : current_user["username"],
                        "forename" : current_user["forename"],
                        "surname" : current_user["surname"],
                        "profile_picture" : current_user["profile_picture"]
                    },
                    "cover_photo" : data["cover_photo"],
                    "description" : data["description"],
                    "text" : data["text"],
                    "comments" : [],
                    "city" : city_for_post
                }

                new_post_id = config.posts.insert_one(new_post)
                new_post_link = "http://localhost:5000" + BASE_URL + "/" + str(new_post_id.inserted_id)
                return make_response( jsonify({"url": new_post_link} ), 201)
    
            else:
                return make_response(jsonify({ "error" : "City not found" }), 404)

        else:
            return make_response(jsonify({ "error" : "Post already exists with this title" }), 409)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["PUT"])
@utils.admin_or_post_owner_required
def edit_post(id):
    try:
        post_with_id = helpers.get_post_by_id(config.posts, id)

        if post_with_id is not None:
            post_with_name = helpers.get_post_by_title(config.posts, request.json["title"])

            if post_with_name is None:
                city_for_post = helpers.get_city_by_id(config.cities, request.json["cityID"])

                if city_for_post:
                    current_user = helpers.get_user_from_mongo_by_username(config.users, os.environ["CURRENT_USER"])
                    updated_post = { "$set" : {
                        "title" : request.json["title"],
                        "author" : {
                            "username" : current_user["username"],
                            "forename" : current_user["forename"],
                            "surname" : current_user["surname"],
                            "profile_picture" : current_user["profile_picture"]
                        },
                        "cover_photo" : request.json["cover_photo"],
                        "description" : request.json["description"],
                        "text" : request.json["text"],
                        "city" : city_for_post
                    }}
                
                    config.posts.update_one({ "_id" : ObjectId(id) }, updated_post)
                    updated_post_link = "http://localhost:5000" + BASE_URL + "/" + id

                    return make_response( jsonify({"url": updated_post_link} ), 201)
                
                else:
                    return make_response(jsonify({ "error" : "City not found" }), 404)
            else:
                return make_response(jsonify( { "error" : "Post with this title already exists" } ), 409)

        else:
            return make_response(jsonify( { "error" : "Post not found" } ), 404)
    
    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["DELETE"])
@utils.admin_or_post_owner_required
def delete_post(id):
    post = helpers.get_post_by_id(config.posts, id)

    if post is not None:
        config.posts.delete_one( { "_id" : ObjectId(id) } )
        return make_response( jsonify( {} ), 200)

    else:
        return make_response(jsonify({ "error" : "Post not found" }), 404)

    
@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["GET"])
def get_comments_on_post(id):
    post = helpers.get_post_by_id(config.posts, id)

    if post is not None:
        page_num, page_size, sort_direction = 1, 5, 1
        
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        
        if request.args.get('sort_direction'):
            sort_direction = int(request.args.get('sort_direction'))

        page_start = (page_size * (page_num - 1))
        page_of_comments = helpers.get_post_comments(post["_id"], config.posts, page_start, page_size, sort_direction)
        return make_response(jsonify( page_of_comments ), 200)
        
    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["POST"])
@utils.check_for_jwt
def add_comment_to_post(id):
    try:
        current_user = helpers.get_user_from_mongo_by_username(config.users, os.environ["CURRENT_USER"])
        post = helpers.get_post_by_id(config.posts, id)

        if post is not None:
            new_comment = {
                "_id" : ObjectId(),
                "username" : current_user["username"],
                "forename" : current_user["forename"],
                "surname" : current_user["surname"],
                "profile_picture" : current_user["profile_picture"],
                "text" : request.get_json()["text"]
            }

            config.posts.update_one( { "_id" : ObjectId(id) }, { "$push" : { "comments" : new_comment } } )
            new_comment_link = BASE_URL + "/" + id + "/comments/" + str(new_comment['_id'])
            return make_response( jsonify({ "url" : new_comment_link } ), 201 )
            
        else:
           return make_response(jsonify( { "error" : "Post not found" } ), 404)    

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/comments/<string:comment_id>", methods=["GET"])
def get_comment_by_id(comment_id):
    comment = helpers.get_post_comment_by_id(config.posts, comment_id)

    if comment is not None:
        return make_response( jsonify(comment), 200)

    else:
        return make_response(jsonify( { "error" : "Comment not found" } ), 404)


@posts_blueprint.route(BASE_URL + "/comments/<string:comment_id>", methods=["PUT"])
@utils.admin_or_comment_owner_required
def edit_comment(comment_id):
    try:
        current_user = helpers.get_user_from_mongo_by_username(config.users, os.environ["CURRENT_USER"])
        comment = helpers.get_post_comment_by_id(config.posts, comment_id)

        if comment is not None:
            edited_comment = {
                "comments.$.username" : current_user["username"],
                "comments.$.forename" : current_user["forename"],
                "comments.$.surname" : current_user["surname"],
                "comments.$.profile_picture" : current_user["profile_picture"],
                "comments.$.text" : request.get_json()["text"],
            }
            
            config.posts.update_one({ "comments._id" : ObjectId(comment_id) }, { "$set" : edited_comment } )
            edit_comment_url = BASE_URL + "/comments/" + comment_id
            return make_response( jsonify( {"url" : edit_comment_url} ), 200)

        else:
            return make_response(jsonify( { "error" : "Comment not found" } ), 404)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)
         

@posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["DELETE"])
@utils.admin_or_comment_owner_required_for_delete
def delete_comment(post_id, comment_id):
    post = helpers.get_post_by_id(config.posts, post_id)
    comment = helpers.get_post_comment_by_id(config.posts, comment_id)

    if post is not None:
        if comment is not None:
            try:
                config.posts.update_one( { "_id" : ObjectId(post_id) }, { "$pull" : { "comments" : { "_id" : ObjectId(comment_id) } } } ) 
                return make_response( jsonify( {} ), 200)

            except:
                return make_response(jsonify( { "error" : "Server failed to delete comment" } ), 500)
        
        else:
            return make_response(jsonify( { "error" : "Comment not found" } ), 404)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)    


@posts_blueprint.route(BASE_URL + "/check-access/<string:id>", methods=["GET"])
@utils.admin_or_post_owner_required_boolean
def check_for_post_owner_or_admin(id):
    if id:
        return make_response( jsonify( True ), 200)
    
    else:
        return make_response(jsonify( False ), 401)
 

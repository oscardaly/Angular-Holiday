from login import utils
from flask import Blueprint, jsonify, make_response, request
from setup_mongodb import config, helpers
from bson import ObjectId

posts_blueprint = Blueprint('posts', __name__)
BASE_URL = "/api/v1.0/posts"


@posts_blueprint.route(BASE_URL, methods=["GET"])
def get_all_posts():
    page_num, page_size = 1, 10
    
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    
    page_start = (page_size * (page_num - 1))
    page_of_posts = config.posts.find().skip(page_start).limit(page_size)
    data_to_return = helpers.get_posts_from_mongo(page_of_posts)
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
        post = helpers.get_post_by_title(config.posts, request.json["title"])

        if post is None:
            new_post = {
                "title" : request.json["title"],
                "author" : {
                    "username" : request.json["author"]["username"],
                    "forename" : request.json["author"]["forename"],
                    "surname" : request.json["author"]["surname"],
                    "user_photo" : request.json["author"]["user_photo"]
                },
                "cover_photo" : request.json["cover_photo"],
                "description" : request.json["description"],
                "text" : request.json["text"],
                "comments" : [],
                "city" : {
                    "name" : request.json["city"]["name"],
                    "population" : "",
                    "latitude" : "",
                    "longitude" : "",
                    "country" : ""
                }
            }

            new_post_id = config.posts.insert_one(new_post)
            new_post_link = "http://localhost:5000" + BASE_URL + "/" + str(new_post_id.inserted_id)
            return make_response( jsonify({"url": new_post_link} ), 201)

        else:
            return make_response(jsonify({ "error" : "Post already exists with this title" }), 409)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["PUT"])
@utils.check_for_jwt
def edit_post(id):
    try:
        post_with_id = helpers.get_post_by_id(config.posts, id)

        if post_with_id is not None:
            post_with_name = helpers.get_post_by_title(config.posts, request.json["title"])

            if post_with_name is None:
                updated_post = { "$set" : {
                    "title" : request.json["title"],
                    "author" : {
                        "username" : request.json["author"]["username"],
                        "forename" : request.json["author"]["forename"],
                        "surname" : request.json["author"]["surname"],
                        "user_photo" : request.json["author"]["user_photo"]
                    },
                    "cover_photo" : request.json["cover_photo"],
                    "description" : request.json["description"],
                    "text" : request.json["text"],
                    "comments" : [],
                    "city" : {
                        "name" : request.json["city"]["name"],
                        "population" : "",
                        "latitude" : "",
                        "longitude" : "",
                        "country" : ""
                    }
                }}

                config.posts.update_one({ "_id" : ObjectId(id) }, updated_post)
                updated_post_link = "http://localhost:5000" + BASE_URL + "/" + id

                return make_response( jsonify({"url": updated_post_link} ), 200)

            else:
                return make_response(jsonify( { "error" : "Post with this title already exists" } ), 409)

        else:
            return make_response(jsonify( { "error" : "Post not found" } ), 404)
    
    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["DELETE"])
@utils.check_for_jwt
def delete_post(id):
    post = helpers.get_post_by_id(config.posts, id)

    if post is not None:
        config.posts.delete_one( { "_id" : ObjectId(id) } )
        return make_response( jsonify( {} ), 204)

    else:
        return make_response(jsonify({ "error" : "Post not found" }), 404)

    
@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["GET"])
def get_comments_on_post(id):
    post = helpers.get_post_by_id(config.posts, id)

    if post is not None:
        post_comments = helpers.get_post_comments(post)

        if len(post_comments) != 0:
            page_num, page_size = 1, 5
            
            if request.args.get('pn'):
                page_num = int(request.args.get('pn'))
            
            if request.args.get('ps'):
                page_size = int(request.args.get('ps'))
            
            page_start = (page_size * (page_num - 1))
            page_of_comments = post_comments[page_start:page_start + page_size]
            
            return make_response(jsonify( page_of_comments ), 200)

        else:
            return make_response(jsonify( { "error" : "No comments found" } ), 404)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["POST"])
@utils.check_for_jwt
def add_comment_to_post(id):
    try:
        post = helpers.get_post_by_id(config.posts, id)

        if post is not None:
            new_comment = {
                "_id" : ObjectId(),
                "username" : request.json["username"],
                "forename" : request.json["forename"],
                "surname" : request.json["surname"],
                "user_photo" : request.json["user_photo"],
                "text" : request.json["text"]
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
@utils.check_for_jwt
def edit_comment(comment_id):
    try:
        comment = helpers.get_post_comment_by_id(config.posts, comment_id)

        if comment is not None:
            edited_comment = {
                "comments.$.username" : request.json["username"],
                "comments.$.forename" : request.json["forename"],
                "comments.$.surname" : request.json["surname"],
                "comments.$.user_photo" : request.json["user_photo"],
                "comments.$.text" : request.json["text"],
            }
            
            config.posts.update_one({ "comments._id" : ObjectId(comment_id) }, { "$set" : edited_comment } )
            edit_comment_url = BASE_URL + "/" + "/comments/" + comment_id
            return make_response( jsonify( {"url" : edit_comment_url} ), 200)

        else:
            return make_response(jsonify( { "error" : "Comment not found" } ), 404)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)
         

@posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["DELETE"])
@utils.check_for_jwt
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
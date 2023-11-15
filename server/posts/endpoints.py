from flask import Blueprint, jsonify, make_response, request
from login import utils
import uuid

posts_blueprint = Blueprint('posts', __name__)

BASE_URL = "/api/v1.0/posts"

posts = {
    "1" : {
        "name" : "My trip to Edinburgh",
        "author" : {
            "forename" : "name",
            "username" : "example username",
            "user_photo" : "example photo"
        },
        "cover_photo" : "photo",
        "description" : "This is a post talking about my recent trip to Edinburgh",
        "text" : "",
        "comments" : {
            "1" : {
                "forename" : "name",
                "text" : "Loved that cafe!"
            }
        },
        "city" : {
            "name" : "Edinburgh",
            "population" : "",
            "latitude" : "",
            "longitude" : "",
            "country" : "Scotland"
        }
    },
    "2" : {
        "name": "Exploring Tokyo",
        "author": {
            "forename": "another name",
            "username": "another username",
            "user_photo": "another photo"
        },
        "cover_photo": "photo",
        "description": "Discovering the beauty of Tokyo",
        "text" : "",
        "comments": {
            "1" : {
                "forename": "another name",
                "text": "Amazing cityscape!"
            }
        },
        "city": {
            "name": "Tokyo",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Japan"
        }
    },
    "3" : {
        "name": "Weekend in Paris",
        "author": {
            "forename": "third name",
            "username": "third username",
            "user_photo": "third photo"
        },
        "cover_photo": "photo",
        "description": "A romantic getaway to the city of love",
        "text" : "",
        "comments": {
            "1" : {
                "forename": "third name",
                "text": "Beautiful pictures!"
            }
        },
        "city": {
            "name": "Paris",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "France"
        }
    },
    "4" : {
        "name": "Hiking in the Swiss Alps",
        "author": {
            "forename": "fourth name",
            "username": "fourth username",
            "user_photo": "fourth photo"
        },
        "cover_photo": "photo",
        "description": "Breath-taking views from the Swiss Alps",
        "text" : "",
        "comments": {
            "1" : {
                "forename": "fourth name",
                "text": "Nature at its finest!"
            }
        },
        "city": {
            "name": "Swiss Alps",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Switzerland"
        }
    },
    "5" : {
        "name": "Safari in Serengeti",
        "author": {
            "forename": "fifth name",
            "username": "fifth username",
            "user_photo": "fifth photo"
        },
        "cover_photo": "photo",
        "description": "Witnessing the wonders of wildlife in Serengeti",
        "text" : "",
        "comments": {
            "1" : {
                "forename": "fifth name",
                "text": "Incredible experience!"
            }
        },
        "city": {
            "name": "Serengeti",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Tanzania"
        }
    }
}


@posts_blueprint.route(BASE_URL, methods=["GET"])
def get_all_posts():
    page_num, page_size = 1, 10
    
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    
    page_start = (page_size * (page_num - 1))
    list_of_posts = [ { k : v } for k, v in posts.items() ]
    page_of_posts = list_of_posts[page_start:page_start + page_size]
    
    return make_response(jsonify( page_of_posts ), 200)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["GET"])
def get_post(id):
    if id in posts:
        return make_response(jsonify(posts[id]), 200)

    else:
        return make_response(jsonify({ "error" : "Post not found" }), 404)


@posts_blueprint.route(BASE_URL, methods=["POST"])
@utils.check_for_jwt
def add_post():
    try:
        post_id = str(uuid.uuid4())
        new_post = {
            "post_name" : request.json["post_name"],
            "author" : {
                "forename" : request.json["author"]["forename"],
                "username" : request.json["author"]["username"],
                "user_photo" : request.json["author"]["user_photo"]
            },
            "cover_photo" : request.json["cover_photo"],
            "description" : request.json["description"],
            "text" : request.json["text"],
            "comments" : {},
            "city" : {
                "name" : request.json["city"]["name"],
                "population" : "",
                "latitude" : "",
                "longitude" : "",
                "country" : ""
            }
        }

        posts[post_id] = new_post
        return make_response(jsonify( { post_id : new_post } ), 201)

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["PUT"])
@utils.check_for_jwt
def edit_post(id):
    try:
        if id in posts:
            new_post = {
                "post_name" : request.json["post_name"],
                "author" : {
                    "forename" : request.json["author"]["forename"],
                    "username" : request.json["author"]["username"],
                    "user_photo" : request.json["author"]["user_photo"]
                },
                "cover_photo" : request.json["cover_photo"],
                "description" : request.json["description"],
                "text" : request.json["text"],
                "comments" : {},
                "city" : {
                    "name" : request.json["city"]["name"],
                    "population" : "",
                    "latitude" : "",
                    "longitude" : "",
                    "country" : ""
                }
            }

            posts[id] = new_post
            return make_response( jsonify( { id : posts[id] } ), 200 )

        else:
            return make_response(jsonify( { "error" : "Post not found" } ), 404)
    
    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>", methods=["DELETE"])
@utils.check_for_jwt
def delete_post(id):
    if id in posts:
        del posts[id]
        return make_response( jsonify( {} ), 204)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)
    

@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["GET"])
def get_comments_on_post(id):
    if id in posts:
        page_num, page_size = 1, 10
        
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        
        page_start = (page_size * (page_num - 1))
        list_of_comments = [ { k : v } for k, v in posts[id]["comments"].items() ]
        page_of_comments = list_of_comments[page_start:page_start + page_size]
        
        return make_response(jsonify( page_of_comments ), 200)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["POST"])
@utils.check_for_jwt
def add_new_comment_on_post(id):
    try:
        if id in posts:
            new_comment_id = str(uuid.uuid4())
            new_comment = {
                "forename" : request.form["forename"],
                "text" : request.form["text"]
            }
            posts[id]["comments"][new_comment_id] = new_comment
            return make_response( jsonify( { new_comment_id : new_comment } ), 201 )
            
        else:
           return make_response(jsonify( { "error" : "Post not found" } ), 404)    

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)


@posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["GET"])
def get_comment_by_id(post_id, comment_id):
    if post_id in posts:
        if comment_id in posts[post_id]["comments"]:
            return make_response(jsonify( { comment_id : posts[post_id]["comments"][comment_id] } ), 200)
        
        else:
            return make_response(jsonify( { "error" : "Comment not found" } ), 404)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)    


@posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["PUT"])
@utils.check_for_jwt
def edit_comment(post_id, comment_id):
    try:
        if post_id in posts:
            if comment_id in posts[post_id]["comments"]:
                posts[post_id]["comments"][comment_id]["forename"] = request.form["forename"]
                posts[post_id]["comments"][comment_id]["text"]= request.form["text"]
                return make_response( jsonify( { comment_id : posts[post_id]["comments"][comment_id] } ), 200)

            else:
                return make_response(jsonify( { "error" : "Comment not found" } ), 404)

        else:
            return make_response(jsonify( { "error" : "Post not found" } ), 404)    

    except:
        return make_response(jsonify( { "error" : "Missing form data" } ), 404)

            

@posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["DELETE"])
@utils.check_for_jwt
def delete_comment(post_id, comment_id):
    if post_id in posts:
        if comment_id in posts[post_id]["comments"]:
            del posts[post_id]["comments"][comment_id]
            return make_response( jsonify( {} ), 200)

        else:
            return make_response(jsonify( { "error" : "Comment not found" } ), 404)

    else:
        return make_response(jsonify( { "error" : "Post not found" } ), 404)    


# generate_password_hash("noONEwillEVERguessTHIS")
# check_password_hash(hashed_password, "noONEwillEVERguessTHIS")

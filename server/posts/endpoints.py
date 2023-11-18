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


# @posts_blueprint.route(BASE_URL + "/<string:id>", methods=["GET"])
# def get_post(id):
#     post = helpers.get_post_from_mongo_by_id(config.posts, postID)

#     if post is not None:
#         return make_response(jsonify(posts), 200)

#     else:
#         return make_response(jsonify({ "error" : "Post not found" }), 404)


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


# @posts_blueprint.route(BASE_URL + "/<string:id>", methods=["DELETE"])
# @utils.check_for_jwt
# def delete_post(id):
#     if id in posts:
#         del posts[id]
#         return make_response( jsonify( {} ), 204)

#     else:
#         return make_response(jsonify( { "error" : "Post not found" } ), 404)
    

# @posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["GET"])
# def get_comments_on_post(id):
#     if id in posts:
#         page_num, page_size = 1, 10
        
#         if request.args.get('pn'):
#             page_num = int(request.args.get('pn'))
        
#         if request.args.get('ps'):
#             page_size = int(request.args.get('ps'))
        
#         page_start = (page_size * (page_num - 1))
#         list_of_comments = [ { k : v } for k, v in posts[id]["comments"].items() ]
#         page_of_comments = list_of_comments[page_start:page_start + page_size]
        
#         return make_response(jsonify( page_of_comments ), 200)

#     else:
#         return make_response(jsonify( { "error" : "Post not found" } ), 404)


# @posts_blueprint.route(BASE_URL + "/<string:id>/comments", methods=["POST"])
# @utils.check_for_jwt
# def add_new_comment_on_post(id):
#     try:
#         if id in posts:
#             new_comment_id = str(uuid.uuid4())
#             new_comment = {
#                 "forename" : request.form["forename"],
#                 "text" : request.form["text"]
#             }
#             posts[id]["comments"][new_comment_id] = new_comment
#             return make_response( jsonify( { new_comment_id : new_comment } ), 201 )
            
#         else:
#            return make_response(jsonify( { "error" : "Post not found" } ), 404)    

#     except:
#         return make_response(jsonify( { "error" : "Missing form data" } ), 404)


# @posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["GET"])
# def get_comment_by_id(post_id, comment_id):
#     if post_id in posts:
#         if comment_id in posts[post_id]["comments"]:
#             return make_response(jsonify( { comment_id : posts[post_id]["comments"][comment_id] } ), 200)
        
#         else:
#             return make_response(jsonify( { "error" : "Comment not found" } ), 404)

#     else:
#         return make_response(jsonify( { "error" : "Post not found" } ), 404)    


# @posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["PUT"])
# @utils.check_for_jwt
# def edit_comment(post_id, comment_id):
#     try:
#         if post_id in posts:
#             if comment_id in posts[post_id]["comments"]:
#                 posts[post_id]["comments"][comment_id]["forename"] = request.form["forename"]
#                 posts[post_id]["comments"][comment_id]["text"]= request.form["text"]
#                 return make_response( jsonify( { comment_id : posts[post_id]["comments"][comment_id] } ), 200)

#             else:
#                 return make_response(jsonify( { "error" : "Comment not found" } ), 404)

#         else:
#             return make_response(jsonify( { "error" : "Post not found" } ), 404)    

#     except:
#         return make_response(jsonify( { "error" : "Missing form data" } ), 404)

            

# @posts_blueprint.route(BASE_URL + "/<string:post_id>/comments/<string:comment_id>", methods=["DELETE"])
# @utils.check_for_jwt
# def delete_comment(post_id, comment_id):
#     if post_id in posts:
#         if comment_id in posts[post_id]["comments"]:
#             del posts[post_id]["comments"][comment_id]
#             return make_response( jsonify( {} ), 200)

#         else:
#             return make_response(jsonify( { "error" : "Comment not found" } ), 404)

#     else:
#         return make_response(jsonify( { "error" : "Post not found" } ), 404)    


# generate_password_hash("noONEwillEVERguessTHIS")
# check_password_hash(hashed_password, "noONEwillEVERguessTHIS")
# make the posts helper to get posts
# set up the db for posts and import it 
from bson import ObjectId

def get_users_from_mongo(users):
    data_to_return = []

    for user in users.find():
        user['_id'] = str(user['_id'])
        user['password'] = ''
        data_to_return.append(user)

    return data_to_return


def get_user_from_mongo_by_username(users, username):
    user = users.find_one({'username' : username})

    if user is not None:
        user['_id'] = str(user['_id'])
        user['password'] = ''

    return user


def get_posts_from_mongo(posts):
    data_to_return = []

    for post in posts:
        post['_id'] = str(post['_id'])
        
        for comment in post['comments']:
            comment['_id'] = str(comment['_id'])
       
        data_to_return.append(post)

    return data_to_return


def get_post_by_title(posts, postTitle):
    try:
        post = posts.find_one({'title' : postTitle})
        
        if post is not None:
            post['_id'] = str(post['_id'])

            for comment in post['comments']:
                comment['_id'] = str(comment['_id'])
        
        return post
    
    except:
        return None


def get_post_by_id(posts, postID):
    try:
        post = posts.find_one({'_id' : ObjectId(postID)})
        
        if post is not None:
            post['_id'] = str(post['_id'])

            for comment in post['comments']:
                comment['_id'] = str(comment['_id'])  
                      
        return post
    
    except:
        return None


def get_post_comments(post):
        post_comments = []
        
        for comment in post["comments"]:
            comment["_id"] = str(comment["_id"])
            post_comments.append(comment)
        
        return post_comments


def get_post_comment_by_id(posts, commentID):
    try:
        comment = posts.find_one( { "comments._id" : ObjectId(commentID) }, { "_id" : 0, "comments.$" : 1 } )
        comment['comments'][0]['_id'] = str(comment['comments'][0]['_id'])
        comment = comment['comments'][0]

        return comment

    except:
        return None
def get_users_from_mongo(users):
    data_to_return = []

    for user in users.find():
        user['_id'] = str(user['_id'])
        data_to_return.append(user)

    return data_to_return

def get_user_from_mongo_by_username(users, username):
    user = users.find_one({'username' : username})

    if user is not None:
        user['_id'] = str(user['_id'])

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
    post = posts.find_one({'title' : postTitle})

    if post is not None:
        post['_id'] = str(post['_id'])

    return post
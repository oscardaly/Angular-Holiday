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

def update_user_object_for_comment_subdocument(user):
    new_user = {}

    for key in user:
        new_key = "comments.$." + key
        new_user[new_key] = user[key]

    return new_user

def get_posts_from_mongo(postsDB, page_size, page_start, sort_by_direction, sort_by_function, title, country, city):
    aggregator = []
    data_to_return = []
    
    if (title):
        aggregator.append({ "$match" : { "title" : title }})

    if (city):
        aggregator.extend([
        { "$unwind" : "$city" },
        { "$match" : 
            { "$or" : [          
                { "city" : city },
                { "city.city_ascii" : city }
            ]}
        }])

    elif (country):
        aggregator.extend([
        { "$unwind" : "$city" },
        { "$match" : 
            {
                "city.country" : country 
            },
        }])

    if (sort_by_function == "comments"):
        sort_by_function = "{ \"$size\" : \"comments\" }"

    if (sort_by_function == "city"):
        sort_by_function =  "city.city"

    aggregator.extend([       
        { "$sort" : { sort_by_function : sort_by_direction } },
        { "$skip" : page_start },
        { "$limit" : page_size }
    ])

    posts = postsDB.aggregate(aggregator)

    for post in posts:
        post = parse_post_from_mongo(post)
        data_to_return.append(post)

    return data_to_return


def get_post_by_title(posts, postTitle):
    try:
        post = posts.find_one({'title' : postTitle})
        
        if post is not None:
            return parse_post_from_mongo(post)
    
    except:
        return None


def get_post_by_id(posts, postID):
    try:
        post = posts.find_one({'_id' : ObjectId(postID)})
        
        if post is not None:
            return parse_post_from_mongo(post)
    
    except:
        return None


def parse_post_from_mongo(post):
    post['_id'] = str(post['_id'])
    post['city']['_id'] = str(post['city']['_id'])
    for comment in post['comments']:
        comment['_id'] = str(comment['_id'])
    
    return post


def get_post_comments(postID, postsDB, page_start, page_size, sort_direction):
    post_comments = postsDB.aggregate([
        { "$match" : { "_id" : ObjectId(postID) }},  
        { "$unwind" : "$comments" },
        { "$project" : { 
            "_id" : "$comments._id", 
            "forename" : "$comments.forename", 
            "surname" : "$comments.surname",
            "text" : "$comments.text",
            "username" : "$comments.username",
            "profile_picture" : "$comments.profile_picture"
        }},
        { "$sort" : { "_id" : sort_direction } },
        { "$skip" : page_start },
        { "$limit" : page_size }
    ])

    data_to_return = []

    for comment in post_comments:
        comment["_id"] = str(comment["_id"])
        data_to_return.append(comment)

    return data_to_return


def get_post_comment_by_id(posts, commentID):
    try:
        comment = posts.find_one( { "comments._id" : ObjectId(commentID) }, { "_id" : 0, "comments.$" : 1 } )
        comment['comments'][0]['_id'] = str(comment['comments'][0]['_id'])
        comment = comment['comments'][0]

        return comment

    except:
        return None

def get_city_by_id(citiesDB, cityID):
    try:
        return citiesDB.find_one({ "id" : cityID })

    except:
        return None
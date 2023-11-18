import json
from bson import ObjectId

users = [
    {
        "username" : "username",
        "forename" : "user",
        "surname" : "surname",
        "password" : "user",
        "profile_picture" : "",
        "type" : "user"
    },
    {
        "username" : "admin",
        "forename" : "admin",
        "surname" : "surname",
        "password" : "admin",
        "profile_picture" : "",
        "type" : "admin"       
    },
    {
        "username" : "dummy",
        "forename" : "dummy",
        "surname" : "surname",
        "password" : "dummy",
        "profile_picture" : "",
        "type" : "user"       
    }
]

fout = open("users.json", "w")
fout.write(json.dumps(users))
fout.close()


posts = [
    {
        "name" : "My trip to Edinburgh",
        "author" : {
            "username" : "example username",
            "forename" : "name",
            "surname" : "surname",
            "user_photo" : "example photo"
        },
        "cover_photo" : "photo",
        "description" : "This is a post talking about my recent trip to Edinburgh",
        "text" : "",
        "comments" : [
            {
                "username" : "example username",
                "forename" : "name",
                "surname" : "surname",
                "user_photo" : "example photo",
                "text" : "Loved that cafe!"
            }
        ],
        "city" : {
            "name" : "Edinburgh",
            "population" : "",
            "latitude" : "",
            "longitude" : "",
            "country" : "Scotland"
        }
    },
    {
        "name": "Exploring Tokyo",
        "author": {
            "username": "another username",
            "forename": "another name",
            "surname" : "surname",
            "user_photo": "another photo"
        },
        "cover_photo": "photo",
        "description": "Discovering the beauty of Tokyo",
        "text" : "",
        "comments": [
            {
                "username" : "example username",
                "forename" : "name",
                "surname" : "surname",
                "text": "Amazing cityscape!"
            }
        ],
        "city": {
            "name": "Tokyo",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Japan"
        }
    },
    {
        "name": "Weekend in Paris",
        "author": {
            "username" : "example username",
            "forename" : "name",
            "surname" : "surname",
            "user_photo": "third photo"
        },
        "cover_photo": "photo",
        "description": "A romantic getaway to the city of love",
        "text" : "",
        "comments": [
            {
                "username" : "example username",
                "forename" : "name",
                "surname" : "surname",
                "text": "Beautiful pictures!"
            }
        ],
        "city" : {
            "name": "Paris",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "France"
        }
    },
    {
        "name": "Hiking in the Swiss Alps",
        "author": {
            "username" : "example username",
            "forename" : "name",
            "surname" : "surname",
            "user_photo": "fourth photo"
        },
        "cover_photo": "photo",
        "description": "Breath-taking views from the Swiss Alps",
        "text" : "",
        "comments": [
            {
                "username" : "example username",
                "forename" : "name",
                "surname" : "surname",
                "text": "Nature at its finest!"
            }
        ],
        "city": {
            "name": "Swiss Alps",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Switzerland"
        }
    },
    {
        "name": "Safari in Serengeti",
        "author": {
           "username" : "example username",
            "forename" : "name",
            "surname" : "surname",
            "user_photo": "fifth photo"
        },
        "cover_photo": "photo",
        "description": "Witnessing the wonders of wildlife in Serengeti",
        "text" : "",
        "comments": [
            {
                "username" : "example username",
                "forename" : "name",
                "surname" : "surname",
                "text": "Incredible experience!"
            }
        ],
        "city": {
            "name": "Serengeti",
            "population": "",
            "latitude": "",
            "longitude": "",
            "country": "Tanzania"
        }
    }
]

fout = open("posts.json", "w")
fout.write(json.dumps(posts))
fout.close()
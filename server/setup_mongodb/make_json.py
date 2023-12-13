from pymongo import MongoClient
from default_posts import default_posts
from default_cities import default_cities
from default_users import default_users
import bcrypt

def main():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.holidayDB
    usersDB = db.users
    postsDB = db.posts
    citiesDB = db.cities

    setup_user_db(usersDB)
    # setup_posts_db(postsDB)
    # setup_cities_db(citiesDB)
    # add_cities_to_default_posts(postsDB, citiesDB)


def setup_user_db(usersDB):
    users = default_users

    for user in users:
        user["password"] = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
        usersDB.insert_one(user)


def setup_posts_db(postsDB):
    posts = default_posts

    for post in posts:
        postsDB.insert_one(post)


def setup_cities_db(citiesDB):
    cities = default_cities
    num_processed = 0

    for city in cities:
        try:
            city.pop("iso3")
            city.pop("admin_name")
            city.pop("capital")

        except:
            print("no capital for " + city["city"])

        finally:
            citiesDB.insert_one(city)
            num_processed = num_processed + 1

            if num_processed % 1000 == 0:
                print(str(num_processed) + " cities processed")


def add_cities_to_default_posts(postsDB, citiesDB):
    num_processed = 0
    for post in postsDB.find({}, { "_id" : 1 , "city.name" : 1 }, no_cursor_timeout = True):
        city = citiesDB.find_one({ "city_ascii" : post["city"]["name"] })
        
        if city == None:
            print(post["city"]["name"])

        postsDB.update_one({ "_id" : post["_id"] }, { "$set" : { "city" : city }})
        
        num_processed = num_processed + 1

        if num_processed % 10 == 0:
            print(str(num_processed) + " cities processed")


if __name__ == "__main__":
    main()
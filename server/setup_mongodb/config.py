from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.holidayDB
users = db.users 
posts = db.posts
blacklist = db.blacklist
cities = db.cities
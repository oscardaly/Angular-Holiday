import os
from flask import Flask
from users.endpoints import users_blueprint
from login.endpoints import login_blueprint
from posts.endpoints import posts_blueprint
from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(users_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(posts_blueprint)

load_dotenv()

app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

if __name__ == "__main__":
    app.run(debug=True)


# delete pycache from repo and add to gitignore
# add dates to posts and comments?
# fix adding images

# If an author of a post or comment updates their details it should update this in their comments and their posts 
# Show extra functionality in the frontend
# Could sort comments by newest/oldest
# create table for cities

# to start db we need to run .env.py, make_json and app
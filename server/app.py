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


# Proper error handling
# Merge token checkers together in another nested wrapper
# create table for cities
#   Infer city values when post created or edited 
# mock up frontend and check that all functionality needed is present in backend
# Add 100+ items using make_json to start app/database
    # add_fields.py to show changing database
# change all errors to use proper error
# Show extra functionality in the frontend

# delete pycache from repo and add to gitignore
# fix adding images

# to start db we need to run .env.py, make_json and app
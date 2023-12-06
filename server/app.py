import os
from flask import Flask
from users.endpoints import users_blueprint
from login.endpoints import login_blueprint
from posts.endpoints import posts_blueprint
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(users_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(posts_blueprint)
CORS(app)

load_dotenv()

app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

if __name__ == "__main__":
    app.run(debug=True)


# add images - C4 page 13
# Proper error handling
# Merge token checkers together in another nested wrapper
# mock up frontend and check that all functionality needed is present in backend
# change all errors to use proper error
# postman tests
# Show extra functionality in the frontend

# delete pycache from repo and add to gitignore
# to start db we need to run .env.py, make_json and app
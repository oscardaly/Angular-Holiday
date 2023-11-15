from flask import Flask
from users.endpoints import users_blueprint
from login.endpoints import login_blueprint
from posts.endpoints import posts_blueprint

app = Flask(__name__)
app.register_blueprint(users_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(posts_blueprint)

API_VERSION = "v1.0"
BASE_URL = "/api/" + API_VERSION
SECRET_KEY = "mysecret"

app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
    app.run(debug=True)


# add app back into certain files to import the secret key from app
# add app back into certain files to import the baseurl from app
# delete pycache from repo and add to gitignore
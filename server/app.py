from flask import Flask

app = Flask(__name__)

API_VERSION = "v1.0"
BASE_URL = "/api/" + API_VERSION
SECRET_KEY = "mysecret"

app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
    app.run(debug=True)

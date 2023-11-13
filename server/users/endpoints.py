from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

users =  {
    "user" : {
        "name" : "user",
        "password" : "user",
        "profile_picture" : "",
        "type" : "user"
    },
    "admin" : {
        "name" : "admin",
        "password" : "admin",
        "profile_picture" : "",
        "type" : "admin"       
    },
    "dummy" : {
        "name" : "dummy",
        "password" : "dummy",
        "profile_picture" : "",
        "type" : "user"       
    }
}

@app.route("/api/v1.0/users", methods=["GET"])
def get_all_users():
    return make_response( jsonify( users ), 200 )


@app.route("/api/v1.0/users/<string:username>", methods=["GET"])
def get_user_by_username(username):
    return make_response( jsonify(  users[username] ), 200 )


@app.route("/api/v1.0/users", methods=["POST"])
def add_user():
        # check for same id/username in backend
        username = request.form["username"]
        new_user = { 
                "name" : request.form["name"],
                "password" : request.form["password"],
                "profile_picture" : request.form["profile_picture"],
                "type" : "user"
        }
        
        users[username] = new_user
        return make_response( jsonify( { username : new_user } ), 201 )


@app.route("/api/v1.0/users/<string:username>", methods=["PUT"])
def edit_user(username):
    users[username]["name"] = request.form["name"]
    users[username]["password"] = request.form["password"]
    users[username]["profile_picture"] = request.form["profile_picture"]
    return make_response( jsonify( { username : users[username] } ), 200 )


@app.route("/api/v1.0/users/<string:username>", methods=["DELETE"])
def delete_user(username):
    del users[username]
    return make_response( jsonify( {} ), 200)


if __name__ == "__main__":
    app.run(debug=True)
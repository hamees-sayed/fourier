from flask import render_template, request
from controllers import app

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "username":
            if password == "password":
                return render_template("success.html")
            else:
                return "Incorrect password!"
        else:
            return "User does not exist."
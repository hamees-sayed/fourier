from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from controllers import app, db
from models import User


@app.route("/register_creator")
def register_creator():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.is_creator = True
        db.session.commit()
        flash("You are now a creator!", "success")
    return redirect(url_for("creator"))

@app.route("/creator")
def creator():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        if user.is_creator:
            return render_template("creator_account.html", title="Creator")
        else:
            flash("Register as a creator first.", "info")
    return redirect(url_for("account"))
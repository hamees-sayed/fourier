from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from controllers.forms import RegistrationForm, LoginForm
from controllers import app, db, bcrypt
from models import User, Playlist


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}, you can now Log in!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form, title="Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    playlists = Playlist.query.all()
    return render_template("user_account.html", title="Account", playlists=playlists, length=len(playlists))
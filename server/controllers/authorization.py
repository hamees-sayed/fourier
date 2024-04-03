import click
import jwt
import json
from datetime import datetime, timedelta
from types import SimpleNamespace
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from flask_login import login_user, current_user, logout_user
from controllers.forms import RegistrationForm, LoginForm
from controllers import app, db, bcrypt
from models import User


@app.cli.command('create-admin')
@click.option('--username', prompt=True, help='Username for the Admin.')
@click.option('--email', prompt=True, help='Email for the Admin.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the Admin.')
def create_admin(username, email, password):
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo(f"Username '{username}' already exists in the database, please choose a different one.")
    elif len(password) < 8:
        click.echo("Password should be atleast 8 characters.")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, is_admin=True)
        db.session.add(new_user)
        db.session.commit()
        click.echo(f"Admin '{username}' created successfully.")

@app.cli.command('delete-admin')
@click.option('--email', prompt=True, help='Email for the Admin.')
@click.option('--password', prompt=True, hide_input=True, help='Password for the Admin.')
def delete_admin(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.is_admin:
        db.session.delete(user)
        db.session.commit()
        click.echo(f"Admin '{user.username}' deleted successfully")
    else:
        click.echo("Admin not found. Check your email or password.")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for("admin"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("admin_login.html", form=form, title="Admin Login", admin=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    json_data = request.get_json()
    data = SimpleNamespace(**json_data)
    
    existing_user = User.query.filter((User.username == data.username) | (User.email == data.email)).first()
    if existing_user:
        return jsonify({"error": {"code": 400, "message": "USER ALREADY EXISTS"}}), 400
    
    hashed_password = bcrypt.generate_password_hash(data.password).decode('utf-8')
    user = User(username=data.username, email=data.email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))

    response = jsonify({"token": access_token, "user_id": user.user_id, "username": user.username, "email": user.email, "is_admin": user.is_admin, "is_creator": user.is_creator})
    print(response)
    return response, 201


@app.route("/login", methods=["GET", "POST"])
def login():
    json_data = request.get_json()
    data = SimpleNamespace(**json_data)
    
    user = User.query.filter_by(email=data.email).first()
    if user and bcrypt.check_password_hash(user.password, data.password):
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))

        response = jsonify({"token": access_token, "user_id": user.user_id, "username": user.username, "email": user.email, "is_admin": user.is_admin, "is_creator": user.is_creator})
        print(response)
        return response, 201
    else:
        return jsonify({ "error" : {'message': 'INVALID CREDENTIALS', 'authenticated': False, 'code': 401 }}), 401


@app.route("/logout")
@jwt_required
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404
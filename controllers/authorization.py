import click
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from controllers.forms import RegistrationForm, LoginForm
from controllers import app, db, bcrypt
from models import User


@app.cli.command('create-admin')
@click.option('--username', prompt=True, default='admin', help='Username for the Admin.')
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404
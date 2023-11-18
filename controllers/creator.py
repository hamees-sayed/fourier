from functools import wraps
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from controllers.forms import NewAlbumForm, UpdateAlbumForm
from controllers import app, db
from models import User, Creator, Album


def creator_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login first.", "info")
            return redirect(url_for("login"))
        elif not current_user.is_creator:
            flash("Register as a creator first.", "info")
            return redirect(url_for("account"))
        return func(*args, **kwargs)

    return decorated_function


@app.route("/register_creator")
def register_creator():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.is_creator = True
        new_creator = Creator(user_id=user.user_id)
        db.session.add(new_creator)
        db.session.commit()
        flash("You are now a creator!", "success")
    return redirect(url_for("creator"))

@app.route("/creator")
@creator_required
def creator():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template("creator_account.html", title="Creator")

@app.route("/album/new", methods=["GET", "POST"])
@creator_required
def new_album():
    form = NewAlbumForm()
    if form.validate_on_submit():
        album_creator = Creator.query.filter_by(user_id=current_user.user_id).first()
        album = Album(creator_id = album_creator.creator_id, album_name=form.album_name.data, genre=form.genre.data)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for("albums"))
    return render_template("new_album.html", form=form, title="New Album")
        
@app.route("/album")
@creator_required
def albums():
    album = Album.query.filter_by(creator_id=current_user.creator.creator_id).all()
    return render_template("creator_albums.html", title="Album", albums = album)
    
@app.route("/album/<int:album_id>/delete")
@creator_required
def delete_album(album_id):
    album = Album.query.get(album_id)
    if album:
        db.session.delete(album)
        db.session.commit()
        flash("Album deleted successfully!", "success")
        return redirect(url_for("albums"))
    else:
        flash("Album not found", "danger")
        return redirect(url_for("albums"))

@app.route("/album/<int:album_id>/update", methods=["GET", "POST"])
@creator_required
def update_album(album_id):
    album = Album.query.get(album_id)
    if album:
        form = UpdateAlbumForm()
        if form.validate_on_submit():
            album.album_name = form.album_name.data
            album.genre = form.genre.data
            db.session.commit()
            flash("Album updated successfully!", "success")
            return redirect(url_for("albums"))
        elif request.method == "GET":
            form.album_name.data = album.album_name
            form.genre.data = album.genre
        return render_template("update_album.html", form=form, title="Update Album", album=album)
    else:
        flash("Album not found", "danger")
        return redirect(url_for("albums"))
from flask import render_template, flash, redirect, url_for
from functools import wraps
from flask_login import current_user, login_required
from controllers import app, db
from models import User, Creator, Song, Album, Rating

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login as an admin first.", "info")
            return redirect(url_for("admin_login"))
        elif not current_user.is_admin:
            return {"message":"unauthorized"}, 401
        return func(*args, **kwargs)
    return decorated_function

@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html")

@app.route("/users")
@admin_required
def users():
    users = User.query.filter_by(is_admin=False, is_creator=False).all()
    return render_template("admin_users.html", users=users)

@app.route("/creators")
@admin_required
def creators():
    creators = Creator.query.all()
    return render_template("admin_creators.html", creators=creators)

@app.route("/admin/songs")
@admin_required
def admin_songs():
    songs_with_ratings = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()
    return render_template("home.html", songs_with_ratings=songs_with_ratings)

@app.route("/admin/albums")
@admin_required
def admin_albums():
    albums = Album.query.all()
    return render_template("admin_albums.html", albums=albums)

@app.route("/user/<int:user_id>/delete")
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("users"))
    else:
        flash("User not found", "info")
        return redirect(url_for("users"))

@app.route("/creator/<int:creator_id>/delete")
@admin_required
def delete_creator(creator_id):
    creator = Creator.query.get(creator_id)
    user = User.query.filter_by(user_id=creator.user_id).first()
    songs = Song.query.filter_by(creator_id=creator.creator_id).all()
    albums = Album.query.filter_by(creator_id=creator.creator_id).all()
    if creator:
        user.is_creator = False
        db.session.delete(creator)
        for song in songs:
            delete_song(song.song_id)
        for album in albums:
            delete_album(album.album_id)
        db.session.commit()
        return redirect(url_for("creators"))
    else:
        flash("Creator not found", "info")
        return redirect(url_for("creators"))

@app.route("/creator/<int:creator_id>/blacklist")
@admin_required
def blacklist_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        creator.is_blacklisted=True
        db.session.commit()
        return redirect(url_for("creators"))
    else:
        flash("Creator not found", "info")
        return redirect(url_for("creators"))

@app.route("/creator/<int:creator_id>/whitelist")
@admin_required
def whitelist_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        creator.is_blacklisted=False
        db.session.commit()
        return redirect(url_for("creators"))
    else:
        flash("Creator not found", "info")
        return redirect(url_for("creators"))

@app.route("/flag/<int:song_id>/song")
@admin_required
def song_flagging(song_id):
    song = Song.query.get(song_id)
    if song:
        if not song.is_flagged:
            song.is_flagged=True
            db.session.commit()
            return redirect(url_for("admin_songs"))
        else:
            song.is_flagged=False
            db.session.commit()
            return redirect(url_for("admin_songs"))
    else:
        flash("Song not found", "info")
        return redirect(url_for("admin_songs"))

@app.route("/flag/<int:album_id>/album")
@admin_required
def album_flagging(album_id):
    album = Album.query.get(album_id)
    if album:
        if album.is_flagged:
            album.is_flagged=False
            db.session.commit()
            return redirect(url_for("admin_albums"))
        else:
            album.is_flagged=True
            db.session.commit()
            return redirect(url_for("admin_albums"))
    else:
        flash("Album not found", "info")
        return redirect(url_for("admin_albums"))

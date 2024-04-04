from flask import flash, redirect, url_for
from flask import jsonify
from controllers import app, db
from controllers.creator import delete_song, delete_album
from models import User, Creator, Song, Album, Rating, Playlist
from controllers.utils import admin_required, current_users_chart, song_rating_histogram


@app.route("/admin")
@admin_required
def admin():
    songs_and_ratings = db.session.query(Song.song_title, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .all()
    if len(songs_and_ratings) == 0:
        song, rating = [], []
    else:
        song, rating = zip(*songs_and_ratings)
        
    rating = [0 if r is None else r for r in rating]
    song_rating_hist = song_rating_histogram(song, rating)

    users = User.query.filter_by(is_admin=False).all()
    current_users_plot = current_users_chart(users)

    users_only = User.query.filter_by(is_admin=False, is_creator=False).all()
    creators = Creator.query.all()
    songs = Song.query.all()
    albums = Album.query.all()

    # return render_template("admin.html", users=len(users_only), creators=len(creators), songs=len(songs), albums=len(albums), current_users_plot=current_users_plot, song_rating_hist=song_rating_hist)
    data = {
        "users": len(users_only),
        "creators": len(creators),
        "songs": len(songs),
        "albums": len(albums),
        "current_users_plot": current_users_plot,
        "song_rating_hist": song_rating_hist
    }

    return jsonify(data)


@app.route("/users")
@admin_required
def users():
    users = User.query.filter_by(is_admin=False, is_creator=False).all()
    # return render_template("admin_users.html", users=users)
    data = []
    for user in users:
        data.append({
            "id": user.user_id,
            "username": user.username,
            "email": user.email,
        })

    return jsonify(data)

@app.route("/creators")
@admin_required
def creators():
    creators = Creator.query.all()
    # return render_template("admin_creators.html", creators=creators)
    data = []
    for creator in creators:
        data.append({
            "id": creator.creator_id,
            "creator_name": creator.user.username,
            "email": creator.user.email,
            "is_blacklisted": True if creator.is_blacklisted else False,
        })
    return jsonify(data)

@app.route("/admin/songs")
@admin_required
def admin_songs():
    songs_with_ratings = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()
    # return render_template("home.html", songs_with_ratings=songs_with_ratings)
    data = []
    for song, average_rating in songs_with_ratings:
        data.append({
            "id": song.song_id,
            "song_title": song.song_title,
            "genre": song.genre,
            "creator": song.creator.user.username if song.creator else None,
            "average_rating": round(average_rating, 2) if average_rating else 0,
            "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
            "song_file_url": url_for('static', filename='songs/'+song.song_file),
            "is_flagged": True if song.is_flagged else False,
        })
    return jsonify(data)


@app.route("/admin/albums")
@admin_required
def admin_albums():
    albums = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id).all()
    # return render_template("admin_albums.html", albums=albums)
    data = []
    for album, creator in albums:
        data.append({
            "id": album.album_id,
            "album_name": album.album_name,
            "genre": album.genre,
            "creator_name": creator.user.username,
            "is_flagged": True if album.is_flagged or album.is_flagged==None else False,
        })
    return jsonify(data)

@app.route("/user/<int:user_id>/delete")
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    ratings = Rating.query.filter_by(user_id=user_id).all()
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    creator = Creator.query.filter_by(user_id=user_id).first()
    if creator:
        flash("User is a creator. Delete the creator first.", "info")
        return redirect(url_for("users"))
    if user:
        db.session.delete(user)
        for rating in ratings:
            db.session.delete(rating)
        for playlist in playlists:
            db.session.delete(playlist)
        db.session.commit()
        return redirect(url_for("users"))
    else:
        flash("User not found", "info")
        return redirect(url_for("users"))

@app.route("/creator/<int:creator_id>/delete")
@admin_required
def delete_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        user = User.query.filter_by(user_id=creator.user_id).first()
        songs = Song.query.filter_by(creator_id=creator.creator_id).all()
        albums = Album.query.filter_by(creator_id=creator.creator_id).all()
        for song in songs:
            delete_song(song.song_id)
        for album in albums:
            delete_album(album.album_id)
        db.session.delete(creator)
        user.is_creator = False
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

from flask import request, url_for
from flask import jsonify
from flask_jwt_extended import jwt_required
from controllers import app, db, cache, redis_client
from controllers.creator import delete_song, delete_album
from models import User, Creator, Song, Album, Rating, Playlist
from controllers.utils import admin_required, current_users_chart, song_rating_histogram


@app.route("/admin")
@jwt_required()
@admin_required
@cache.cached(timeout=90, key_prefix='admin_dashboard')
def admin():
    cached_response = redis_client.get('admin_dashboard')
    if cached_response:
        return jsonify(cached_response)
    
    songs_and_ratings = db.session.query(
        Song.song_title,
        db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .filter(Song.is_flagged == False) \
        .group_by(Song.song_title).all()
    
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
@jwt_required()
@admin_required
@cache.cached(timeout=90, key_prefix='users')
def users():
    cached_response = redis_client.get('users')
    if cached_response:
        return jsonify(cached_response)
    
    users = User.query.filter_by(is_admin=False, is_creator=False).all()
    data = []
    for user in users:
        data.append({
            "id": user.user_id,
            "username": user.username,
            "email": user.email,
        })

    return jsonify(data)

@app.route("/creators")
@jwt_required()
@admin_required
@cache.cached(timeout=90, key_prefix='creators')
def creators():
    cached_response = redis_client.get('creators')
    if cached_response:
        return jsonify(cached_response)
    
    creators = Creator.query.all()
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
@jwt_required()
@admin_required
@cache.cached(timeout=90, key_prefix='admin_songs')
def admin_songs():
    cached_response = redis_client.get('admin_songs')
    if cached_response:
        return jsonify(cached_response)
    
    songs_with_ratings = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()

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
@jwt_required()
@admin_required
@cache.cached(timeout=90, key_prefix='admin_albums')
def admin_albums():
    cached_response = redis_client.get("admin_albums")
    if cached_response:
        return jsonify(cached_response)
        
    albums = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id).all()
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
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.filter(User.user_id==user_id, User.is_creator==False, User.is_admin==False).first()
    ratings = Rating.query.filter_by(user_id=user_id).all()
    playlists = Playlist.query.filter_by(user_id=user_id).all()

    if user:
        db.session.delete(user)
        for rating in ratings:
            db.session.delete(rating)
        for playlist in playlists:
            db.session.delete(playlist)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "USER NOT FOUND"}}), 400

@app.route("/creator/<int:creator_id>/delete")
@jwt_required()
@admin_required
def delete_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        user = User.query.filter_by(user_id=creator.user_id).first()
        songs = Song.query.filter_by(creator_id=creator.creator_id).all()
        albums = Album.query.filter_by(creator_id=creator.creator_id).all()
        for song in songs:
            delete_song(song.song_file)
        for album in albums:
            delete_album(album.album_id)
        db.session.delete(creator)
        user.is_creator = False
        db.session.commit()
        return jsonify({"message": "Creator deleted successfully"}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "CREATOR NOT FOUND"}}), 400

@app.route("/creator/<int:creator_id>/blacklist")
@jwt_required()
@admin_required
def blacklist_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        creator.is_blacklisted=True
        db.session.commit()
        return jsonify({"message": "Creator blacklisted successfully", "creator_id": creator_id}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "CREATOR NOT FOUND"}}), 400

@app.route("/creator/<int:creator_id>/whitelist")
@jwt_required()
@admin_required
def whitelist_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if creator:
        creator.is_blacklisted=False
        db.session.commit()
        return jsonify({"message": "Creator whitelisted successfully", "creator_id": creator_id}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "CREATOR NOT FOUND"}}), 400

@app.route("/flag/<int:song_id>/song")
@jwt_required()
@admin_required
def song_flagging(song_id):
    song = Song.query.get(song_id)
    if song:
        if not song.is_flagged:
            song.is_flagged=True
            db.session.commit()
            return jsonify({"message": "Song flagged successfully", "song_id": song_id}), 200
        else:
            song.is_flagged=False
            db.session.commit()
            return jsonify({"message": "Song unflagged successfully", "song_id": song_id}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400

@app.route("/flag/<int:album_id>/album")
@jwt_required()
@admin_required
def album_flagging(album_id):
    album = Album.query.get(album_id)
    if album:
        if album.is_flagged:
            album.is_flagged=False
            db.session.commit()
            return jsonify({"message": "Album unflagged successfully", "song_id": album_id}), 200
        else:
            album.is_flagged=True
            db.session.commit()
            return jsonify({"message": "Album flagged successfully", "song_id": album_id}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400
    
@app.route("/admin/search")
@jwt_required()
@admin_required
def song_search_admin():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .join(Creator, Song.creator_id == Creator.creator_id) \
        .filter((Song.song_title.like(query)) | (Song.lyrics.like(query)) | (Creator.user.has(username=search_term)) | (Song.genre.like(query))) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()

    data = []
    for song, average_rating in search_result:
        data.append({
            "song_title": song.song_title,
            "genre": song.genre,
            "creator_username": song.creator.user.username if song.creator else None,
            "average_rating": round(average_rating, 2) if average_rating else 0,
            "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
            "song_file_url": url_for('static', filename='songs/' + song.song_file),
            "song_id": song.song_id,
            "is_flagged": song.is_flagged,
            "creator_id": song.creator.creator_id,
            "creator_is_blacklisted": song.creator.is_blacklisted
        })
    return jsonify(data)

@app.route("/admin/albums/search")
@jwt_required()
@admin_required
def album_search_admin():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id) \
    .filter(
        (
            (Album.album_name.like(query)) |
            (Album.genre.like(query)) |
            (Creator.user.has(username=search_term))
        )
    ).all()

    data = []
    for album, creator in search_result:
        data.append({
            "id": album.album_id,
            "album_name": album.album_name,
            "genre": album.genre,
            "album_creator": creator.user.username,
        })
    return jsonify(data)
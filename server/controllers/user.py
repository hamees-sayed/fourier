from flask import url_for, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from types import SimpleNamespace
from controllers import app, db
from models import User, Song, Playlist, Playlist_song, Creator, Rating


@app.route("/account")
@jwt_required()
def account():
    current_user = get_jwt_identity()
    playlists = Playlist.query.filter_by(user_id=current_user).all()
    data = []
    if playlists:
        for playlist in playlists:
            data.append({
                "id": playlist.playlist_id,
                "playlist_name": playlist.playlist_name,
                "playlist_desc": playlist.playlist_desc,
            })
    return jsonify(data)

@app.route("/register_creator", methods=["GET", "POST"])
@jwt_required()
def register_creator():
    user = get_jwt_identity()
    current_user = User.query.filter_by(user_id=user).first()
    if not current_user.is_creator:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            json_data = request.get_json()
            data = SimpleNamespace(**json_data)
            user.username = data.username
            user.is_creator = True
            new_creator = Creator(user_id=user.user_id)
            db.session.add(new_creator)
            db.session.commit()
            return jsonify({"user_id": user.user_id, "username": user.username, "email": user.email, "is_admin": user.is_admin, "is_creator": user.is_creator}), 201
    else:
        return jsonify({"error": {"code": 400, "message": "CREATOR ALREADY EXISTS"}}), 400

@app.route("/playlist/new", methods=["GET", "POST"])
@jwt_required()
def new_playlist():
    user = get_jwt_identity()
    current_user = User.query.filter_by(user_id=user).first()
    if current_user:
        json_data = request.get_json()
        data = SimpleNamespace(**json_data)
        playlist = Playlist(user_id = current_user.user_id, playlist_name=data.playlist_name, playlist_desc=data.playlist_desc)
        db.session.add(playlist)
        db.session.commit()
        return jsonify({"playlist_id": playlist.playlist_id, "playlist_name": playlist.playlist_name, "playlist_desc": playlist.playlist_desc}), 201

@app.route("/playlist/<int:playlist_id>/delete")
@jwt_required()
def delete_playlist(playlist_id):
    user = get_jwt_identity()
    current_user = User.query.filter_by(user_id=user).first()
    if current_user:
        playlist = Playlist.query.get(playlist_id)
        songs_in_playlist = Playlist_song.query.filter_by(playlist_id=playlist_id).all()
        if playlist:
            for song in songs_in_playlist:
                db.session.delete(song)
            db.session.delete(playlist)
            db.session.commit()
            return jsonify({"message": "Success. Playlist Deleted."}), 200
        else:
            return jsonify({"error": {"code": 400, "message": "PLAYLIST NOT FOUND"}}), 400

@app.route("/playlist/<int:playlist_id>/update", methods=["GET", "POST"])
@jwt_required()
def update_playlist(playlist_id):
    current_user = get_jwt_identity()
    playlist = Playlist.query.filter_by(playlist_id=playlist_id, user_id=current_user).first()
    if playlist:
        json_data = request.get_json()
        data = SimpleNamespace(**json_data)
        playlist.playlist_name = data.playlist_name
        playlist.playlist_desc = data.playlist_desc

        db.session.commit()
        return jsonify({"playlist_id": playlist.playlist_id, "playlist_name": playlist.playlist_name, "playlist_desc": playlist.playlist_desc}), 201
    else:
        return jsonify({"error": {"code": 400, "message": "PLAYLIST NOT FOUND"}}), 400
    

@app.route("/playlist/add/<int:song_id>", methods=['GET', 'POST'])
@jwt_required()
def add_to_playlist(song_id):
    user = get_jwt_identity()
    current_user = User.query.filter_by(user_id=user).first()
    song = Song.query.get(song_id)

    if song:
        json_data = request.get_json()
        data = SimpleNamespace(**json_data)
        new_playlist_song = Playlist_song(playlist_id=data.playlist_id, song_id=song_id)
        db.session.add(new_playlist_song)
        db.session.commit()
        return jsonify({"playlist_id": new_playlist_song.playlist_id, "song_id": new_playlist_song.song_id}), 201
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400

@app.route("/playlist/<int:playlist_id>")
@jwt_required()
def get_playlist(playlist_id):
    songs_in_playlist = Song.query.join(Playlist_song) \
        .join(Creator, Song.creator_id == Creator.creator_id) \
        .filter(
            Playlist_song.playlist_id == playlist_id,
            Song.is_flagged == False,
            Creator.is_blacklisted == False
        ).all()
    current_user = get_jwt_identity()
    playlist = Playlist.query.filter_by(playlist_id=playlist_id, user_id=current_user).first()
    if not playlist:
        return jsonify({"error": {"code": 400, "message": "PLAYLIST NOT FOUND"}}), 400

    data = []
    if songs_in_playlist:
        for song in songs_in_playlist:
            data.append({
                    "song_title": song.song_title,
                    "genre": song.genre,
                    "creator_username": song.creator.user.username if song.creator else None,
                    "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
                    "song_file_url": url_for('static', filename='songs/' + song.song_file),
                    "song_id": song.song_id
                })
    return jsonify(data)

@app.route("/rate/<int:song_id>", methods=["GET", "POST"])
@jwt_required()
def rate_song(song_id):
    user = get_jwt_identity()
    current_user = User.query.filter_by(user_id=user).first()
    song = Song.query.get(song_id)
    already_rated = Rating.query.filter_by(user_id=current_user.user_id, song_id=song_id).first()
    if already_rated:
        return jsonify({"error": {"code": 400, "message": "ALREADY RATED"}}), 400
    if song:
        json_data = request.get_json()
        data = SimpleNamespace(**json_data)
        new_rating = Rating(rating=data.rating, user_id=current_user.user_id, song_id=song_id)
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({"rating": new_rating.rating, "user_id": new_rating.user_id, "song_id": new_rating.song_id}), 201
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400
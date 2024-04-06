from flask import flash, url_for, request
from flask import jsonify
from types import SimpleNamespace
from flask_jwt_extended import jwt_required
from controllers import app, db
from models import Creator, Album, Song, Rating
from controllers.utils import creator_required, save_song_file, delete_song_file, song_duration, song_rating_histogram, current_user_instance, creator_or_admin


@app.route("/creator")
@jwt_required()
@creator_required
def creator():
    current_user = current_user_instance()
    songs = Song.query.filter_by(creator_id=current_user.creator.creator_id).count()
    albums = Album.query.filter_by(creator_id=current_user.creator.creator_id).count()
    songs_and_ratings = db.session.query(Song.song_title, Rating.rating).join(Rating).filter(Song.creator_id == current_user.creator.creator_id).all()
    if len(songs_and_ratings) == 0:
        song, rating = [], []
    else:
        song, rating = zip(*songs_and_ratings)
        
    rating = [0 if r is None else r for r in rating]
    song_rating_hist = song_rating_histogram(song, rating)
    data = {
        "username": current_user.username,
        "num_of_songs": songs,
        "num_of_albums": albums,
        "song_rating_hist": song_rating_hist
    }
    return jsonify(data)

@app.route("/album/new", methods=["GET", "POST"])
@jwt_required()
@creator_required
def new_album():
    json_data = request.get_json()
    data = SimpleNamespace(**json_data)
    current_user = current_user_instance()
    album_creator = Creator.query.filter_by(user_id=current_user.user_id).first()

    # Check if an album with the same name already exists for the current user
    existing_album = Album.query.filter_by(creator_id=album_creator.creator_id, album_name=data.album_name).first()
    if existing_album:
        return jsonify({"error": {"code": 400, "message": "ALBUM ALREADY EXISTS"}}), 400

    # Create a new album if it doesn't exist
    album = Album(creator_id=album_creator.creator_id, album_name=data.album_name, genre=data.album_genre)
    db.session.add(album)
    db.session.commit()

    return jsonify({
        "creator_id": album.creator_id,
        "album_id": album.album_id,
        "album_name": album.album_name,
        "album_genre": album.genre,
        "is_flagged": album.is_flagged
    }), 200
        
@app.route("/album")
@jwt_required()
@creator_required
def albums():
    current_user = current_user_instance()
    albums = Album.query.filter_by(creator_id=current_user.creator.creator_id).order_by(Album.created_at.desc()).all()
    data = []
    if len(albums) != 0:
        for album in albums:
            data.append({
                "id": album.album_id,
                "title": album.album_name,
                "genre": album.genre,
            })
    return jsonify(data)
    
@app.route("/album/<int:album_id>/delete")
@jwt_required()
@creator_or_admin
def delete_album(album_id):
    current_user = current_user_instance()
    album = Album.query.filter(Album.creator_id == current_user.creator.creator_id, Album.album_id == album_id).first()
    if album:
        db.session.delete(album)
        db.session.commit()
        return jsonify({"message": "Album deleted successfully!"}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "ALBUM NOT FOUND"}}), 400

@app.route("/album/<int:album_id>/update", methods=["GET", "POST"])
@jwt_required()
@creator_required
def update_album(album_id):
    current_user = current_user_instance()
    json_data = request.get_json()
    data = SimpleNamespace(**json_data)
    album = Album.query.filter(Album.album_id==album_id, Album.creator_id==current_user.creator.creator_id).first()
    if album:
        album.album_name = data.album_name
        album.genre = data.album_genre
        db.session.commit()
        return jsonify({
            "creator_id": album.creator_id,
            "album_id": album.album_id,
            "album_name": album.album_name,
            "album_genre": album.genre,
            "is_flagged": album.is_flagged
        }), 200
    else:
        return jsonify({"error": {"code": 400, "message": "ALBUM NOT FOUND"}}), 400

@app.route("/song/new", methods=["GET", "POST"])
@jwt_required()
@creator_required
def new_song():
    current_user = current_user_instance()
    if 'song_file' not in request.files:
        return jsonify({"error": {"code": 400, "message": "MISSING SONG FILE"}}), 400

    # Extract data from form
    song_title = request.form.get('song_title')
    genre = request.form.get('song_genre')
    album_id = request.form.get('album_id', 0)
    lyrics = request.form.get('lyrics', "Lyrics not available.")
    song_file = request.files['song_file']

    # Validate input data
    if not song_title or not genre or not song_file:
        return jsonify({"error": {"code": 400, "message": "MISSING DATA"}}), 400

    # Save song file
    song_file_name = save_song_file(song_file)

    # Create new Song instance
    song = Song(
        album_id=album_id,
        creator_id=current_user.creator.creator_id,
        song_title=song_title,
        genre=genre,
        song_file=song_file_name,
        lyrics=lyrics,
        duration=song_duration(song_file_name)
    )

    # Add song to database
    db.session.add(song)
    db.session.commit()

    # Construct response JSON
    response_data = {
        "id": song.song_id,
        "title": song.song_title,
        "genre": song.genre,
        "lyrics": song.lyrics if song.lyrics else "Lyrics not available",
        "song_file_url": url_for('static', filename='songs/' + song.song_file),
        "is_flagged": song.is_flagged
    }

    return jsonify(response_data), 200


@app.route("/song")
@jwt_required()
@creator_required
def songs():
    current_user = current_user_instance()
    songs = Song.query.filter_by(creator_id=current_user.creator.creator_id).order_by(Song.created_at.desc()).all()
    data = []
    if len(songs) != 0:
        for song in songs:
            data.append({
                "id": song.song_id,
                "title": song.song_title,
                "genre": song.genre,
                "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
                "song_file_url": url_for('static', filename='songs/'+song.song_file),
                "is_flagged": True if song.is_flagged else False,
            })
    return jsonify(data)

@app.route("/song/<int:song_id>/delete")
@jwt_required()
@creator_or_admin
def delete_song(song_id):
    current_user = current_user_instance()
    song = Song.query.filter(Song.creator_id == current_user.creator.creator_id, Song.song_id == song_id).first()
    if song:
        rating = Rating.query.filter_by(song_id=song_id).all()
        for rate in rating:
            db.session.delete(rate)
        delete_song_file(song.song_file)
        db.session.delete(song)
        db.session.commit()
        return jsonify({"message": "Song deleted successfully!"}), 200
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400


@app.route("/song/<int:song_id>/update", methods=["GET", "POST"])
@jwt_required()
@creator_required
def update_song(song_id):
    current_user = current_user_instance()
    json_data = request.get_json()
    data = SimpleNamespace(**json_data)
    song = Song.query.filter(Song.song_id==song_id, Song.creator_id==current_user.creator.creator_id).first()
    if song:
        album_id = data.album_id
        if not data.album_id or data.album_id == 0:
            album_id = 0
        song.album_id = album_id
        song.song_title = data.song_title
        song.genre = data.song_genre
        song.lyrics = data.song_lyrics
        db.session.commit()
        flash('Song updated successfully!', 'success')
        return jsonify({
            "id": song.song_id,
            "title": song.song_title,
            "genre": song.genre,
            "lyrics": song.lyrics if song.lyrics else "Lyrics not available",
        })
    else:
        return jsonify({"error": {"code": 400, "message": "SONG NOT FOUND"}}), 400

@app.route("/album/<int:album_id>")
@jwt_required()
@creator_required
def get_album(album_id):
    current_user = current_user_instance()
    songs = Song.query.filter_by(album_id=album_id).all()
    album = Album.query.filter(Album.album_id==album_id, Album.creator_id==current_user.creator.creator_id).first()
    data = []
    if len(songs) != 0:
        for song in songs:
            data.append({
                "id": song.song_id,
                "album_name": album.album_name,
                "album_genre": album.genre,
                "title": song.song_title,
                "genre": song.genre,
                "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
                "song_file_url": url_for('static', filename='songs/'+song.song_file),
                "is_flagged": True if song.is_flagged else False,
            })
    return jsonify(data)
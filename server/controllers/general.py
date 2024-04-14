from flask import request, url_for
from flask import jsonify
from flask_jwt_extended import jwt_required
from controllers import app, db, cache, redis_client
from models import Album, Song, Creator, Rating


@app.route('/albums')
@jwt_required()
@cache.cached(timeout=90, key_prefix='albums')
def home_albums():
    cached_response = redis_client.get('albums')
    if cached_response:
        return jsonify(cached_response)
    
    albums = db.session.query(Album, Creator)\
    .join(Creator, Album.creator_id == Creator.creator_id)\
    .filter(Album.is_flagged == False, Creator.is_blacklisted == False)\
    .all()
    
    data = []
    if len(albums) != 0:
        for album, creator in albums:
            data.append({
                "id": album.album_id,
                "title": album.album_name,
                "genre": album.genre,
                "album_creator": creator.user.username,
            })
    return jsonify(data)

@app.route("/albums/<int:album_id>")
@jwt_required()
def get_home_album(album_id):    
    songs = Song.query.filter_by(album_id=album_id).all()
    album = Album.query.get(album_id)
    
    album_data = {
        "id": album.album_id,
        "album_creator": album.album_name,
        "genre": album.genre,
    }

    songs_data = []
    for song in songs:
        songs_data.append({
            "id": song.song_id,
            "title": song.song_title,
            "genre": song.genre,
            "lyrics": song.lyrics if song.lyrics else "Lyrics not Available",
            "song_file_url": url_for('static', filename='songs/'+song.song_file),
        })

    return jsonify({
        "album": album_data,
        "songs": songs_data
    })

@app.route('/')
@jwt_required()
@cache.cached(timeout=90, key_prefix='home')
def home():
    cached_response = redis_client.get('home')
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


@app.route("/search")
@jwt_required()
def song_search():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .join(Creator, Song.creator_id == Creator.creator_id) \
        .filter((Song.song_title.like(query)) | (Song.lyrics.like(query)) | (Creator.user.has(username=search_term)) | (Song.genre.like(query))) \
        .filter(Song.is_flagged == False).group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()

    data = []
    for song, average_rating in search_result:
        if song.creator and not (song.is_flagged or song.creator.is_blacklisted):
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

@app.route("/albums/search")
@jwt_required()
def album_search():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id) \
    .filter(
        (
            (Album.album_name.like(query)) |
            (Album.genre.like(query)) |
            (Creator.user.has(username=search_term))
        ) & 
        (Album.is_flagged == False)
    ).all()

    data = []
    for album, creator in search_result:
        if not(album.is_flagged or creator.is_blacklisted):
            data.append({
            "id": album.album_id,
            "title": album.album_name,
            "genre": album.genre,
            "album_creator": creator.user.username,
        })
    return jsonify(data)
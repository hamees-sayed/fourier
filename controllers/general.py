from flask import render_template, request
from flask_login import current_user, login_required
from controllers import app, db
from models import Album, Song, User, Creator, Rating

# count = 0

@app.route('/albums')
@login_required
def home_albums():
    albums = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id).all()
    print(albums[2][1].__dict__)
    return render_template("home_albums.html", title="Albums", albums=albums)

@app.route("/albums/<int:album_id>")
@login_required
def get_home_album(album_id):
    songs = Song.query.filter_by(album_id=album_id).all()
    album = Album.query.get(album_id)
    return render_template("home_album_songs.html", length=len(songs), songs=songs, album=album)

@app.route('/')
def home():
    songs_with_ratings = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()

    return render_template("home.html", title="Home", songs_with_ratings=songs_with_ratings)

@app.route("/search")
@login_required
def song_search():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
    .outerjoin(Rating, Song.song_id == Rating.song_id) \
    .filter((Song.song_title.like(query)) | (Song.lyrics.like(query)) | (Creator.user.has(username=search_term))) \
    .group_by(Song.song_id) \
    .order_by(Song.created_at.desc()) \
    .all()

    return render_template("search_song.html", title="Search", search_result=search_result)

@app.route("/albums/search")
@login_required
def album_search():
    search_term = request.args.get('q')
    query = f"%{search_term}%"

    search_result = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id) \
                    .filter((Album.album_name.like(query)) | (Album.genre.like(query)) | (Creator.user.has(username=search_term))).all()
    
    return render_template("search_album.html", title="Albums", search_result=search_result)
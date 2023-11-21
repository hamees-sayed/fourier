from flask import render_template
from flask_login import current_user, login_required
from controllers import app, db
from models import Album, Song, User, Creator, Rating

# count = 0

@app.route('/albums')
@login_required
def home_albums():
    albums = db.session.query(Album, Creator).join(Creator, Album.creator_id == Creator.creator_id).all()
    return render_template("home_albums.html", title="Albums", albums=albums)

@app.route('/')
def home():
    songs_with_ratings = db.session.query(Song, db.func.avg(Rating.rating).label('average_rating')) \
        .outerjoin(Rating, Song.song_id == Rating.song_id) \
        .group_by(Song.song_id) \
        .order_by(Song.created_at.desc()) \
        .all()

    return render_template("home.html", title="Home", songs_with_ratings=songs_with_ratings)
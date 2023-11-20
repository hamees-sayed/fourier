from flask import render_template
from flask_login import current_user, login_required
from controllers import app, db
from models import Album, Song, User, Creator, Rating

@app.route('/albums')
@login_required
def home_albums():
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return render_template("home_albums.html", title="Albums", albums=albums)

@app.route('/')
def home():
    songs = Song.query.order_by(Song.created_at.desc()).all()
    # Have to implement average rating
    return render_template("home.html", title="Home", songs=songs)

# @app.route('/play/<int:song_id>')
# def play_counter(song_id):
#     song = Song.query.filter_by(song_id=song_id).first()
#     print(song.song_file)
#     return redirect(url_for('home'))
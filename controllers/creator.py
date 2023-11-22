import os
import uuid
import base64
from io import BytesIO
from functools import wraps
from mutagen.mp3 import MP3
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from controllers.forms import NewAlbumForm, UpdateAlbumForm, NewSongForm, UpdateSongForm
from controllers import app, db
from models import User, Creator, Album, Song, Rating


def creator_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login first.", "info")
            return redirect(url_for("login"))
        elif not (current_user.is_creator or current_user.is_admin):
            flash("Register as a creator first.", "info")
            return redirect(url_for("account"))
        return func(*args, **kwargs)
    return decorated_function

def save_song_file(song_file):
    random_string = str(uuid.uuid4().hex[:10])
    base, extension = os.path.splitext(song_file.filename)
    song_fn = f"{random_string}{extension}"
    current_file_path = os.path.abspath(__file__)
    root_path = os.path.abspath(os.path.join(current_file_path, '..', '..'))
    song_path = os.path.join(root_path, 'static/songs', song_fn)
    song_file.save(song_path)

    return song_fn

def delete_song_file(file_name):
    try:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "static", "songs", file_name)
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        return False
    
def song_duration(file_name):
    current_file_path = os.path.abspath(__file__)
    app_root_path = os.path.abspath(os.path.join(current_file_path, '..', '..'))
    songs_folder_path = os.path.join(app_root_path, 'static/songs')
    song_file_path = os.path.join(songs_folder_path, file_name)

    audio = MP3(song_file_path)
    duration_in_seconds = audio.info.length
    return duration_in_seconds

def song_rating_histogram(song, rating):
    """
    Plots a Histogram of Song titles and the corresponding rating
    """
    fig = Figure()
    fig, ax = plt.subplots()
    ax.bar(song, rating)
    ax.set_xlabel('Song Title')
    ax.set_ylabel('Rating')
    ax.set_title('Song Performance')
    buf = BytesIO()
    fig.savefig(buf, format="png")

    return base64.b64encode(buf.getbuffer()).decode("ascii")

@app.route("/creator")
@creator_required
def creator():
    user = User.query.filter_by(username=current_user.username).first()
    songs = Song.query.filter_by(creator_id=current_user.creator.creator_id).count()
    albums = Album.query.filter_by(creator_id=current_user.creator.creator_id).count()

    songs_and_ratings = db.session.query(Song.song_title, Rating.rating).join(Rating).filter(Song.creator_id == current_user.creator.creator_id).all()
    song, rating = zip(*songs_and_ratings)
    song_rating_hist = song_rating_histogram(song, rating)

    return render_template("creator_account.html", songs=songs, albums=albums, song_rating_hist=song_rating_hist, title="Creator")

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
    album = Album.query.filter_by(creator_id=current_user.creator.creator_id).order_by(Album.created_at.desc()).all()
    return render_template("creator_albums.html", title="Album", albums = album, length=len(album))
    
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

@app.route("/song/new", methods=["GET", "POST"])
@creator_required
def new_song():
    form = NewSongForm()
    creator_albums = Album.query.filter_by(creator_id=current_user.creator.creator_id).all()

    form.album.choices = [(str(album.album_id), album.album_name) for album in creator_albums]
    form.album.choices.append(('0', 'Release as Single'))

    if form.validate_on_submit():
        album_id = form.album.data
        if not album_id or album_id == 0:
            album_id = 0

        song_file = save_song_file(form.song_file.data)
        song = Song(
            album_id=album_id,
            creator_id=current_user.creator.creator_id,
            song_title=form.song_title.data,
            song_file=song_file,
            lyrics=form.lyrics.data,
            duration=song_duration(song_file)
        )
        db.session.add(song)
        db.session.commit()
        return redirect(url_for("songs"))

    return render_template("new_song.html", form=form, title="New Song", albums=creator_albums)

@app.route("/song")
@creator_required
def songs():
    song = Song.query.filter_by(creator_id=current_user.creator.creator_id).order_by(Song.created_at.desc()).all()
    return render_template("creator_songs.html", title="Album", songs = song, length=len(song))

@app.route("/song/<int:song_id>/delete")
@creator_required
def delete_song(song_id):
    song = Song.query.get(song_id)
    rating = Rating.query.filter_by(song_id=song_id).all()
    if song:
        delete_song_file(song.song_file)
        db.session.delete(song)
        for rate in rating:
            db.session.delete(rate)
        db.session.commit()
        flash("Song deleted successfully!", "success")
        if current_user.is_admin:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("songs"))
    else:
        flash("Song not found", "danger")
        return redirect(url_for("songs"))


@app.route("/song/<int:song_id>/update", methods=["GET", "POST"])
@creator_required
def update_song(song_id):
    song = Song.query.get(song_id)
    if song:
        creator_albums = Album.query.filter_by(creator_id=current_user.creator.creator_id).all()
        form = UpdateSongForm(obj=song)
        form.album.data = song.album_id

        form.album.choices = [(str(album.album_id), album.album_name) for album in creator_albums]
        form.album.choices.append(('0', 'Release as Single'))

        if form.validate_on_submit():
            album_id = form.album.data
            if not album_id or album_id == 0:
                album_id = 0

            song.album_id = album_id
            song.song_title = form.song_title.data
            song.lyrics = form.lyrics.data

            db.session.commit()
            flash('Song updated successfully!', 'success')
            return redirect(url_for("songs"))
        return render_template("update_song.html", form=form, title="Update Song", song=song)
    else:
        flash("Song not found", "danger")
        return redirect(url_for("songs"))

@app.route("/album/<int:album_id>")
@creator_required
def get_album(album_id):
    songs = Song.query.filter_by(album_id=album_id).all()
    album = Album.query.get(album_id)
    return render_template("album_songs.html", length=len(songs), songs=songs, album=album)
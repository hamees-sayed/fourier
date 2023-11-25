from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from controllers import app, db
from controllers.utils import user_required
from controllers.forms import NewPlaylistForm, UpdatePlaylistForm, RegisterCreator, AddSongToPlaylist, RateSong
from models import User, Song, Playlist, Playlist_song, Creator, Rating


@app.route("/account")
@user_required
def account():
    playlists = Playlist.query.filter_by(user_id=current_user.user_id).all()
    return render_template("user_account.html", title="Account", playlists=playlists, length=len(playlists))

@app.route("/register_creator", methods=["GET", "POST"])
@user_required
def register_creator():
    if not current_user.is_creator:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            form = RegisterCreator()
            if form.validate_on_submit():
                user.username = form.username.data
                user.is_creator = True
                new_creator = Creator(user_id=user.user_id)
                db.session.add(new_creator)
                db.session.commit()
                flash("You are now a creator!", "success")
                return redirect(url_for('creator'))
            elif request.method == 'GET':
                form.username.data = user.username
            return render_template('register_creator.html', form=form, title="Register Creator")
    else:
        flash("You are already a creator!", "info")
    return redirect(url_for("creator"))

@app.route("/playlist/new", methods=["GET", "POST"])
@user_required
def new_playlist():
    form = NewPlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(user_id = current_user.user_id, playlist_name=form.playlist_name.data, playlist_desc=form.playlist_desc.data)
        db.session.add(playlist)
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("new_playlist.html", form=form, title="New Playlist")

@app.route("/playlist/<int:playlist_id>/delete")
@user_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        flash("Playlist deleted successfully!", "success")
        return redirect(url_for("account"))
    else:
        flash("Playlist not found", "info")
        return redirect(url_for("account"))

@app.route("/playlist/<int:playlist_id>/update", methods=["GET", "POST"])
@user_required
def update_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        form = UpdatePlaylistForm(obj=playlist)
        if form.validate_on_submit():
            playlist.playlist_name = form.playlist_name.data
            playlist.playlist_desc = form.playlist_desc.data

            db.session.commit()
            flash('Playlist updated successfully!', 'success')
            return redirect(url_for("account"))
        return render_template("update_playlist.html", form=form, title="Update Playlist", playlist=playlist)
    else:
        flash("Playlist not found", "info")
        return redirect(url_for("account"))

@app.route("/playlist/add/<int:song_id>", methods=['GET', 'POST'])
@user_required
def add_to_playlist(song_id):
    user_playlists = Playlist.query.filter_by(user_id=current_user.user_id).all()
    song = Song.query.get(song_id)

    if song:
        form = AddSongToPlaylist()
        form.playlist.choices = [(str(playlist.playlist_id), playlist.playlist_name) for playlist in user_playlists]
        if form.validate_on_submit():
            new_playlist_song = Playlist_song(playlist_id=form.playlist.data, song_id=song_id)
            db.session.add(new_playlist_song)
            db.session.commit()
            flash("Song added to playlist successfully", "success")
            return redirect(url_for("account"))
    else:
        flash("Song not found", "info")
        return redirect(url_for("home"))

    return render_template("add_to_playlist.html", form=form, song=song, title="Add Song to Playlist")

@app.route("/playlist/<int:playlist_id>")
@user_required
def get_playlist(playlist_id):
    songs_in_playlist = Song.query.join(Playlist_song).filter(Playlist_song.playlist_id==playlist_id).all()
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        flash("Playlist doesn't exist", "info")
        return redirect(url_for("account"))
    return render_template("playlist_songs.html", length=len(songs_in_playlist), songs=songs_in_playlist, playlist=playlist)

@app.route("/rate/<int:song_id>", methods=["GET", "POST"])
@user_required
def rate_song(song_id):
    song = Song.query.get(song_id)
    already_rated = Rating.query.filter_by(user_id=current_user.user_id, song_id=song_id).first()
    if already_rated:
        flash("You already rated this song.", "info")
        return redirect(url_for("home"))
    if song:
        form = RateSong()
        if form.validate_on_submit():
            new_rating = Rating(rating=form.rating.data, user_id=current_user.user_id, song_id=song_id)
            db.session.add(new_rating)
            db.session.commit()
            flash("Rating given successfully.", "success")
            return redirect(url_for("home"))
    else:
        flash("Song not found", "info")
        return redirect(url_for("home"))

    return render_template('rate.html', form=form, song=song, title='Rate Song')
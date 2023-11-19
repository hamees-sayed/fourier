from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from controllers import app, db
from controllers.forms import NewPlaylistForm, UpdatePlaylistForm
from models import User, Song, Playlist, Playlist_song

@app.route("/register_creator")
@login_required
def register_creator():
    if not current_user.is_creator:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            user.is_creator = True
            new_creator = Creator(user_id=user.user_id)
            db.session.add(new_creator)
            db.session.commit()
            flash("You are now a creator!", "success")
    else:
        flash("You are already a creator!", "info")
    return redirect(url_for("creator"))

@app.route("/playlist/new", methods=["GET", "POST"])
@login_required
def new_playlist():
    form = NewPlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(user_id = current_user.user_id, playlist_name=form.playlist_name.data, playlist_desc=form.playlist_desc.data)
        db.session.add(playlist)
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("new_playlist.html", form=form, title="New Playlist")

@app.route("/playlist/<int:playlist_id>/delete")
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        flash("Playlist deleted successfully!", "success")
        return redirect(url_for("account"))
    else:
        flash("Playlist not found", "danger")
        return redirect(url_for("account"))

@app.route("/playlist/<int:playlist_id>/update", methods=["GET", "POST"])
@login_required
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
        flash("Playlist not found", "danger")
        return redirect(url_for("account"))

@app.route("/playlist/<int:playlist_id>")
@login_required
def get_playlist(playlist_id):
    songs_in_playlist = Song.query.join(Playlist_song).filter(Playlist_song.playlist_id==playlist_id).all()
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        flash("Playlist doesn't exist", "info")
        return redirect(url_for("account"))
    return render_template("playlist_songs.html", length=len(songs_in_playlist), songs=songs_in_playlist, playlist=playlist)
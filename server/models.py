from datetime import datetime
from flask_login import UserMixin
from controllers import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_creator = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creator = db.relationship("Creator", backref="user", uselist=False)

    def get_id(self):
        return (self.user_id)

class Creator(db.Model):
    __tablename__ = "creator"
    creator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    songs = db.relationship('Song', backref='creator')
    
class Rating(db.Model):
    __tablename__ = "rating"
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, db.CheckConstraint("rating >= 1 AND rating <= 5"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), nullable=False)

class Album(db.Model):
    __tablename__ = "album"
    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"), nullable=False)
    album_name = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_flagged = db.Column(db.Boolean, nullable=True, default=False)
    songs = db.relationship('Song', backref='album')

class Song(db.Model):
    __tablename__ = "song"
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.album_id"), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"), nullable=False)
    song_title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    song_file = db.Column(db.String(20), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)

class Playlist(db.Model):
    __tablename__ = "playlist"
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    playlist_name = db.Column(db.String(100), nullable=False)
    playlist_desc = db.Column(db.String(300), nullable=True)

class Playlist_song(db.Model):
    __tablename__ = "playlist_song"
    playlist_song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.playlist_id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), nullable=False)
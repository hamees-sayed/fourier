from datetime import datetime
from controllers import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_creator = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
    genre = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    songs = db.relationship('Song', backref='album')

class Song(db.Model):
    __tablename__ = "song"
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.album_id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"), nullable=False)
    song_title = db.Column(db.String(100), nullable=False)
    song_file = db.Column(db.String(20), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    play_counter = db.Column(db.Integer, nullable=False)
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    ratings = db.relationship('User', secondary='rating')

class Playlist(db.Model):
    __tablename__ = "playlist"
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    playlist_name = db.Column(db.String(100), nullable=False)
    songs = db.relationship('Song', secondary='playlist_song')

class Playlist_song(db.Model):
    __tablename__ = "playlist_song"
    playlist_song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.playlist_id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), nullable=False)
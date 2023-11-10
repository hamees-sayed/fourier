from controllers import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_creator = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    playlists = db.relationship('Playlist', backref='user', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', cascade='all, delete-orphan')

class Creator(db.Model):
    __tablename__ = "creator"
    creator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    is_blacklisted = db.Column(db.Boolean, nullable=False)
    songs = db.relationship('Song', backref='creator', cascade='all, delete-orphan')
    
class Rating(db.Model):
    __tablename__ = "rating"
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), nullable=False)
    rating = db.Column(db.Integer, db.CheckConstraint("rating >= 1 AND rating <= 5"), nullable=False)
    ratings = db.relationship('Rating', backref='song', cascade='all, delete-orphan')
    db.UniqueConstraint('user_id', 'song_id')

class Album(db.Model):
    __tablename__ = "album"
    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"), nullable=False)
    album_name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    songs = db.relationship('Song', backref='album', cascade='all, delete-orphan')

class Song(db.Model):
    __tablename__ = "song"
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.album_id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"), nullable=False)
    song_title = db.Column(db.String, nullable=False)
    song_file = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    play_counter = db.Column(db.Integer, nullable=False)
    is_flagged = db.Column(db.Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)

class Playlist(db.Model):
    __tablename__ = "playlist"
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    playlist_name = db.Column(db.String, nullable=False)
    playlist_songs = db.relationship('Playlist_song', backref='playlist', cascade='all, delete-orphan')

class Playlist_song(db.Model):
    __tablename__ = "playlist_song"
    playlist_song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.playlist_id"), primary_key=True, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), primary_key=True, nullable=False)
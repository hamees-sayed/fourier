from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User, Album

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username is taken. Please choose a different one.")
    
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError("User with that email already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
    
class NewAlbumForm(FlaskForm):
    album_name = StringField('Album Name', validators=[DataRequired(), Length(min=2, max=100)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Album')

    def validate_album_name(self, album_name):
        album = Album.query.filter_by(album_name = album_name.data).first()
        if album:
            raise ValidationError("Album Name is taken. Please choose a different one.")

class UpdateAlbumForm(FlaskForm):
    album_name = StringField('Album Name', validators=[DataRequired(), Length(min=2, max=100)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Album')

class NewSongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired(), Length(min=2, max=100)])
    song_file = FileField('Upload a Song', validators=[FileRequired(), FileAllowed(['mp3'])])
    lyrics = TextAreaField('Add Lyrics', validators=[DataRequired()])
    album = RadioField('Select Album', coerce=int)
    submit = SubmitField('Create Song')

class UpdateSongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired(), Length(min=2, max=100)])
    song_file = FileField('Upload a Song', validators=[FileRequired(), FileAllowed(['mp3'])])
    lyrics = TextAreaField('Add Lyrics', validators=[DataRequired()])
    album = RadioField('Select Album', coerce=int)
    submit = SubmitField('Update Song')

class NewPlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist Name', validators=[DataRequired(), Length(min=2, max=100)])
    playlist_desc = StringField('Playlist Description', validators=[Length(min=0, max=300)])
    submit = SubmitField('Create Playlist')

class UpdatePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist Name', validators=[DataRequired(), Length(min=2, max=100)])
    playlist_desc = StringField('Playlist Description', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update Playlist')

class AddSongToPlaylist(FlaskForm):
    playlist = RadioField('Select Playlist', coerce=int)

class RateSong(FlaskForm):
    rating = RadioField('Select Rating', coerce=int)
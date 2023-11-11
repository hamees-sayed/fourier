import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__, template_folder="../templates")
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'database.sqlite3')}"
db = SQLAlchemy(app)
# db.init_app(app)
app.app_context().push()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from controllers import authorization
from controllers import forms
from models import User, Creator, Rating, Album, Song, Playlist, Playlist_song
import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder="../templates", static_folder = "../static")
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'database.sqlite3')}"
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from controllers import authorization, forms, creator, user, general, admin
from models import User, Creator, Rating, Album, Song, Playlist, Playlist_song
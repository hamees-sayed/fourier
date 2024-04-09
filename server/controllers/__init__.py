import os
import redis
from flask import Flask
from celery import Celery
from flask_cors import CORS
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from controllers import workers 

app = Flask(__name__, template_folder="../templates", static_folder = "../static")
CORS(app)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
cache = Cache(app=app)
cache.init_app(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
jwt = JWTManager(app)
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'database.sqlite3')}"
db = SQLAlchemy(app)
app.app_context().push()

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['result_backend'] = 'redis://localhost:6379/2'
app.config['broker_connection_retry_on_startup'] = True
app.config['imports']=('controllers.tasks',)
app.config['timezone']='Asia/Kolkata'
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['result_backend']
)
celery.Task = workers.ContextTask

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from controllers import authorization, forms, creator, user, general, admin, utils
from models import User, Creator, Rating, Album, Song, Playlist, Playlist_song
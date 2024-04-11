import os
import uuid
import base64
from io import BytesIO
from flask import jsonify
from mutagen.mp3 import MP3
from functools import wraps
import matplotlib.pyplot as plt
from datetime import date, timedelta
from matplotlib.figure import Figure
from flask_jwt_extended import get_jwt_identity

from models import User

# Current User instance, replacement for flask_login's current_user
def current_user_instance():
    user = get_jwt_identity()
    return User.query.filter_by(user_id=user).first()

# Decorators
def creator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = current_user_instance()
        if current_user and current_user.is_creator:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": {"code": 401, "message": "NOT A CREATOR"}}), 401
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = current_user_instance()
        if current_user and current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": {"code": 401, "message": "NOT AN ADMIN"}}), 401
    return wrapper

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = current_user_instance()
        if current_user and not (current_user.is_admin or current_user.is_creator):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": {"code": 401, "message": "ACTION NOT ALLOWED"}}), 401
    return wrapper

def creator_or_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = current_user_instance()
        if current_user and (current_user.is_creator or current_user.is_admin):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": {"code": 401, "message": "NOT A CREATOR OR ADMIN"}}), 401
    return wrapper

# song management
def save_song_file(song_file):
    random_string = str(uuid.uuid4().hex[:10])
    _, extension = os.path.splitext(song_file.filename)
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

# Plot Graphs
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
    ax.set_ylim(0, 5)
    buf = BytesIO()
    fig.savefig(buf, format="png")

    return base64.b64encode(buf.getbuffer()).decode("ascii")

def current_users_chart(users):
    """
    Plots a Line chart of Cumulative Users Growth Over Time
    """
    fig = Figure()

    # Get the current date
    current_date = date.today()

    # Initialize data for the cumulative line chart
    dates = [current_date - timedelta(days=i) for i in range(6, -1, -1)]  # Past 7 days
    user_counts = [sum(1 for user in users if user.created_at.date() <= date) for date in dates]

    # Create a cumulative line chart
    fig, ax = plt.subplots()
    ax.plot(range(1, 8), user_counts, marker='o')  # Representing days as 1, 2, ..., 7
    ax.set_ylabel('Cumulative Number of Users')
    ax.set_title('Cumulative Users Growth Over the Past 7 Days')

    # Set y-axis ticks to integer values starting from 0
    max_users = max(user_counts)
    ax.set_yticks(range(max_users + 1))
    ax.set_yticklabels(range(max_users + 1))

    # Save the figure to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return base64.b64encode(buf.read()).decode("ascii")
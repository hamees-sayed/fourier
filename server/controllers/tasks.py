from jinja2 import Template

from controllers import db
from controllers import celery
from controllers.emails import send_email
from models import User, Creator, Album, Song, Rating
from controllers.utils import get_monthly_song_uploads, get_monthly_album_uploads, get_monthly_avg_song_rating, song_rating_histogram

@celery.task()
def mail_users():
    users = User.query.filter(User.is_admin == False).all()
    
    template = Template(open('./templates/user_email.html').read())
    subject = "🎶 Ready to Rock? Fourier Invites You to Tune In! 🎸"
    
    for user in users:
        msg = template.render(username=user.username)
        send_email(user.email, subject=subject, body=msg)
        
@celery.task()
def mail_creators():
    users = User.query.filter(User.is_creator).all()
    
    for user in users:
        albums = Album.query.filter_by(creator_id=user.creator.creator_id).count()
        songs = Song.query.filter_by(creator_id=user.creator.creator_id).count()
        monthly_song_uploads = get_monthly_song_uploads(user.creator.creator_id)
        monthly_album_uploads = get_monthly_album_uploads(user.creator.creator_id)
        monthly_avg_song_rating = get_monthly_avg_song_rating(user.creator.creator_id)
        
        songs_and_ratings = db.session.query(Song.song_title, Rating.rating).join(Rating).filter(Song.creator_id == user.creator.creator_id).all()
        if songs_and_ratings:
            song_titles, ratings = zip(*songs_and_ratings)
        else:
            song_titles, ratings = [], []
        ratings = [0 if r is None else r for r in ratings]
        song_rating_hist = song_rating_histogram(song_titles, ratings)
        
        template = Template(open('./templates/creator_report.html').read())
        subject = "Your Monthly Creator Report 📈"
        
        msg = template.render(
            creator_name=user.username,
            albums=albums,
            songs=songs,
            monthly_song_uploads=monthly_song_uploads,
            monthly_album_uploads=monthly_album_uploads,
            monthly_avg_song_rating=monthly_avg_song_rating,
            song_rating_hist=song_rating_hist
        )
        
        send_email(user.email, subject=subject, body=msg)
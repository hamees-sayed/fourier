from jinja2 import Template

from models import User
from controllers import celery
from controllers.emails import send_email

@celery.task()
def mail_users():
    users = User.query.filter(User.is_admin == False).all()
    
    template = Template(open('./templates/user_email.html').read())
    subject = "🎶 Ready to Rock? Fourier Invites You to Tune In! 🎸"
    
    for user in users:
        msg = template.render(username=user.username)
        send_email(user.email, subject=subject, body=msg)
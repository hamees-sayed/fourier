from celery.schedules import crontab
from controllers import app, celery
from controllers.tasks import mail_users

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        mail_users.s(), 
        name="Sends email everyday at 7:30 PM."
    )

if __name__ == "__main__":
    app.run(debug=True)
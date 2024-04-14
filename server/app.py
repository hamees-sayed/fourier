from celery.schedules import crontab
from controllers import app, celery
from controllers.tasks import mail_users, mail_creators

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        #crontab(hour=19, minute=30),
        10.0,
        mail_users.s(), 
        name="Sends email everyday at 7:30 PM."
    )
    
    sender.add_periodic_task(
        # crontab(0, 0, day_of_month='1'),
        10.0,
        mail_creators.s(), 
        name="Sends Report on the first day of every month."
    )

if __name__ == "__main__":
    app.run(debug=True)
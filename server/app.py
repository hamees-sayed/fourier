from celery.schedules import crontab
from controllers import app, celery
from controllers.tasks import print_hello_world

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, print_hello_world.s(), name="add every 10 seconds")

if __name__ == "__main__":
    app.run(debug=True)
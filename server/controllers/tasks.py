import pytz
from datetime import datetime
from celery.schedules import crontab
from controllers.workers import celery

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, print_current_time_job.s(), name="add every 10 seconds")

@celery.task()
def print_current_time_job():
    print("START")
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now()
    print("now in task = ", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    print("COMPLETE")
    return dt_string
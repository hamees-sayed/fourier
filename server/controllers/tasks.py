from controllers import celery

@celery.task()
def print_hello_world():
    print("Hello World!")
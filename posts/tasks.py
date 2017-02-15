from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add():
    print('aloha')
    return 'tralalala'


from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour=21, minute=50, day_of_week="mon"))
def every_monday_morning():
    print("This is run every Monday morning at 7:30")
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .daily_admin_email import email_report
from .publish_scheduled_posts import automatic_publish

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute=1, hour=0)),
    name="publish_scheduled_posts",
    ignore_result=True
)
def publish_posts():
    automatic_publish()
    logger.info("posts were automatically published")

@periodic_task(
    run_every=(crontab(minute=1, hour=1)),
    name="email_admin",
    ignore_result=True
)
def daily_admin_email():
    email_report()
    logger.info("email to admin has been sent")
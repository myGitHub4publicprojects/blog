from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .daily_admin_email import email_report

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute=1, hour=8)),
    name="email_admin",
    ignore_result=True
)
def daily_admin_email():
    email_report()
    logger.info("email to admin has been sent")
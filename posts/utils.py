import datetime
import math
import re
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

def words_count(html_content):
    stripped = strip_tags(html_content)
    words = re.findall(r'\w+', stripped)
    return len(words)

def read_time(html_content):
    words = words_count(html_content)
    time_in_min = math.ceil(words/220) # assume 220 words per minute
    return int(time_in_min)

def email_report():
    today = datetime.datetime.now().date()
    subject = 'Summary of posts published on %s'%today
    posts_published = 1
    posts_created = 2
    message = 'Today %s posts were published and %s posts were created'%(posts_published, posts_created)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER, # from email
        [settings.MY_EMAIL], # to email
        fail_silently=False,
    )
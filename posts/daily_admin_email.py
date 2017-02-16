import datetime
from django.conf import settings
from django.core.mail import send_mail
from .models import Post

def email_report():
    yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
    subject = 'Summary of posts published on %s'%yesterday
    posts_published_obj = Post.objects.filter(published=yesterday)
    posts_titles = ['"' + post.title + '"' for post in posts_published_obj]
    posts_titles = ', '.join(posts_titles)
    posts_created_obj = Post.objects.filter(timestamp__contains=yesterday)
    created = [post.title for post in posts_created_obj]
    created = ', '.join(created)
    message = 'Yesterday the following posts were published: %s and the following posts were created: %s'%(
        posts_titles,
        created)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER, # from email
        [settings.MY_EMAIL], # to email
        fail_silently=False,
    )
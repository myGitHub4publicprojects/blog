import datetime
from mixer.backend.django import mixer
import pytest
from django.test import TestCase
from django.core import mail

from ..models import Post
from ..daily_admin_email import email_report

pytestmark = pytest.mark.django_db


class TestDailyAdminEmail(TestCase):
    def test_email_report(self):
        'should send email to admin with proper title and message'
        today = datetime.datetime.now().date()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        post1 = mixer.blend('posts.Post', title='post 1 title',
                                        published=yesterday.date())
        post2 = mixer.blend('posts.Post', title='post 2 title')
        # in Post model timestamp has auto_now_add=True so first create instance and update it
        post2.timestamp=yesterday
        post2.save()

        email_subject = 'Summary of posts published on %s'%yesterday.date()
        posts_published_obj = Post.objects.filter(published=yesterday.date())
        posts_titles = ['"' + post.title + '"' for post in posts_published_obj]
        posts_titles = ', '.join(posts_titles)
        posts_created_obj = Post.objects.filter(timestamp__contains=yesterday.date())
        created = ['"' + post.title + '"' for post in posts_created_obj]
        created = ', '.join(created)
        email_message = ('Yesterday the following posts were published: %s, '% posts_titles)+(
                        'and the following posts were created: %s.'% created)
        email_report()
        sent_email = mail.outbox[0]
        assert len(mail.outbox) == 1
        assert sent_email.subject == email_subject
        assert sent_email.body == email_message


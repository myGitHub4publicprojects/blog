from django.test import TestCase
from django.urls import reverse
import datetime
from .models import Post
from django.contrib.auth.models import User

today = datetime.datetime.now().date()
user = User.objects.all().first()

class PostHome(TestCase):
    def test_active_post(self):
        """
        Queryset for the home view for non-staff users should contain only posts with
        published in the past and draft=False. This is achived by PostManager.
        This test creates three posts, one with published in future, one with publihed in past
        and one wih published past but with draft set as True, if 'active' method of
        PostManager works qs generated by filtering posts shold have the same content
        as qs generated by 'active' method
        """
        now = datetime.datetime.now()
        post_yesterday = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        post_tomorrow = Post.objects.create(
            published=today + datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        post_yesterday_draft = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            draft=True,
            title='some title',
            content='some content',
            author=user)
        active_posts = Post.objects.active()
        filtered_objects = Post.objects.filter(draft=False, published__lte=now)
        # two querysets are always different even when contain same info, change them to list
        self.assertEqual(list(active_posts), list(filtered_objects))

class PostDetailTests(TestCase):
    def test_post_detail_published_in_future(self):
        """
        A post with a published in the future should
        return a 404 not found for non-staff users.
        """
        post = Post.objects.create(
            published=today + datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_published_in_past(self):
        """
        A post with a published in the past should
        be visible for staff and non-staff users.
        Testing if response.status_code is 200
        """
        post = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_published_draft(self):
        """
        A post with a published in the past but with draft=True should
        return a 404 not found for non-staff users.
        """
        post = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            draft=True,
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_published_in_past_no_draft(self):
        """
        A post with a published in the past should
        display a post for staff and non-staff users.
        Testing if post.title is in response
        """
        post = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, post.title)
from django.test import TestCase
from django.urls import reverse
import datetime
from .models import Post
from django.contrib.auth.models import User

today = datetime.datetime.now().date()
user = User.objects.all().first()

class PostHome(TestCase):
    def test_active_post(self):
        """ checks if active() method of PostManager works """  
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
        post = Post.objects.create(
            published=today + datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_published_in_past(self):
        post = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_published_draft(self):
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
        post = Post.objects.create(
            published=today - datetime.timedelta(days=1),
            title='some title',
            content='some content',
            author=user)
        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, post.title)
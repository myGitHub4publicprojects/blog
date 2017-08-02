from django.test import TestCase
from django.urls import reverse
import datetime
from posts.models import Post
from django.contrib.auth.models import User


from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
import pytest

from django.contrib.messages import get_messages  

pytestmark = pytest.mark.django_db

now = datetime.datetime.now()

from .. import views
class TestHomeView(TestCase):
    def test_anonymous(self):
        post_yesterday = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_tomorrow = mixer.blend('posts.Post',
                                    published=now + datetime.timedelta(days=1),)
        post_yesterday_draft = mixer.blend('posts.Post',
                                            published=now - datetime.timedelta(days=1),
                                            draft=True,)
        url = reverse('posts:home')
        response = self.client.get(url)
        active_posts = Post.objects.active()
        assert response.status_code == 200, 'Should be callable by anyone'
        # anonymous user should only see active posts (active_posts)
        self.assertEqual(list(response.context['post_list']), list(active_posts))
        
    def test_staff(self):
        post_yesterday = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_tomorrow = mixer.blend('posts.Post',
                                    published=now + datetime.timedelta(days=1),)
        post_yesterday_draft = mixer.blend('posts.Post',
                                            published=now - datetime.timedelta(days=1),
                                            draft=True,)
        user = User.objects.create_user(is_staff=True,
                                        username='adminuser', 
                                        email='oo@gmail.com',
                                        password='somepass')
        # You'll need to log him in before you can send requests through the client
        logged_in = self.client.login(username='adminuser', password='somepass')
        url = reverse('posts:home')
        response = self.client.get(url)
        # staff user should see all posts
        self.assertEqual(len(list(response.context['post_list'])), 3)

    def test_search_anonymous(self):
        post_yesterday = mixer.blend('posts.Post',
                                    content='past content 1',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday2 = mixer.blend('posts.Post',
                                    content='some old content 2',
                                    published=now - datetime.timedelta(days=1),)
        post_tomorrow = mixer.blend('posts.Post',
                                    content='future content 1',
                                    published=now + datetime.timedelta(days=1),)
        post_yesterday_draft = mixer.blend('posts.Post',
                                            content='draft content 1',
                                            published=now - datetime.timedelta(days=1),
                                            draft=True,)
        data={'q': 'past'}
        url = reverse('posts:home')
        response = self.client.get(url, data)
        self.assertEqual(len(response.context['post_list']), 1)
    
    def test_calendar_filter_anonymous(self):
        post_yesterday = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday2 = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_tomorrow = mixer.blend('posts.Post',
                                    published=now + datetime.timedelta(days=1),)
        post_yesterday_draft = mixer.blend('posts.Post',
                                            published=now - datetime.timedelta(days=1),
                                            draft=True,)
        category1 = mixer.blend('posts.Category', name='category1')
        post_yesterday.category.add(category1)
        post_tomorrow.category.add(category1)
        post_yesterday_draft.category.add(category1)
        url = reverse('posts:category', kwargs={'category': 'category1'})
        response = self.client.get(url)
        # anonymous user should see only one (post_yesterday) post
        self.assertEqual(len(response.context['post_list']), 1)
        
    def test_archives_filter_anonymous(self):
        post_march_2011 = mixer.blend('posts.Post',
                                    published=datetime.date(2011, 3, 1))
        post_april_2011 = mixer.blend('posts.Post',
                                    published=datetime.date(2011, 4, 1))
        post_march_2011_draft = mixer.blend('posts.Post',
                                            published=datetime.date(2011, 3, 1),
                                            draft=True,)

        url = reverse('posts:archives', kwargs={'pk': 'Mar2011'})
        response = self.client.get(url)
        # anonymous user should see only one (post_march_2011) post
        self.assertEqual(len(response.context['post_list']), 1)

    def test_pagination_items_per_page_anonymous(self):
        post_yesterday = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday2 = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday3 = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        data = {'iitems': '2'}
        url = reverse('posts:home')
        response = self.client.get(url, data)
        # should show only two posts per page
        self.assertEqual(len(response.context['post_list']), 2)

    def test_pagination_page_over_9999_anonymous(self):
        post_yesterday = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday2 = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        post_yesterday3 = mixer.blend('posts.Post',
                                    published=now - datetime.timedelta(days=1),)
        data = {'iitems': '2', 'page': '99999'}
        url = reverse('posts:home')
        response = self.client.get(url, data)
        # should show last page (2) with only one post
        self.assertEqual(len(response.context['post_list']), 1)

class TestAboutUsView(TestCase):
    def test_anonymous(self):
        '''anonymous users should have access to this view'''
        url = reverse('posts:about-us')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestContactUsView(TestCase):
    def test_anonymous(self):
        '''anonymous users should have access to this view'''
        url = reverse('posts:contact-us')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestPrivacyView(TestCase):
    def test_anonymous(self):
        '''anonymous users should have access to this view'''
        url = reverse('posts:privacy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestCreateView(TestCase):
    def test_anonymous(self):
        '''should generete an 404 error for non staff users'''
        url = reverse('posts:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_staff_user_get(self):
        pass

    def test_staff_user_post(self):
        staff_user = User.objects.create_superuser(is_staff=True,
                                                email='oo@gm.com',
                                                username='staffuser',
                                                password='somepass')
        logged_in = self.client.login(username='staffuser', password='somepass')
        category = mixer.blend('posts.Category')
        # post = mixer.blend('posts.Post', content='old content')
        
        today = datetime.date.today()
        data={'content': 'new content',
            'author': staff_user.pk,
            'title': 'some title',
            'published': today,
            'read_time': 1,
            'category': [category.pk],}
        url = reverse('posts:create')
        response = self.client.post(url, data)

        self.assertTrue(staff_user.is_superuser)
        self.assertTrue(logged_in)
        # read post again from db afer saving changes
        post = Post.objects.first()
        self.assertEqual(post.content, 'new content')

class TestDetailView(TestCase):
    def test_anonymous_with_past_and_active_post(self):
        # create past and active post
        post_yesterday_active = mixer.blend('posts.Post',
            content='XYZ content',
            published=now - datetime.timedelta(days=1),)
        response = self.client.get(reverse('posts:detail', args=(post_yesterday_active.id,)))
        assert response.status_code ==200, 'Should be callable by anyone'
        self.assertContains(response, 'XYZ content')

    def test_anonymous_with_past_and_draft_post(self):
        # create past and draft post
        post_yesterday_draft = mixer.blend('posts.Post',
            draft=True,
            published=now - datetime.timedelta(days=1),)
        response = self.client.get(reverse('posts:detail', args=(post_yesterday_draft.id,)))
        assert response.status_code ==404, 'Should generate 404 error'

    def test_anonymous_with_future_post(self):
        # create past and active post
        post_tomorrow = mixer.blend('posts.Post',
            published=now + datetime.timedelta(days=1),)
        response = self.client.get(reverse('posts:detail', args=(post_tomorrow.id,)))
        assert response.status_code ==404, 'Should generate 404 error'
        
    def test_staff_user_with_future_post(self):
        # create staff user
        user = User.objects.create_user(is_staff=True,
                                        username='adminuser', 
                                        email='oo@gmail.com',
                                        password='oleKolewski12')
        # You'll need to log him in before you can send requests through the client
        logged_in = self.client.login(username='adminuser', password='oleKolewski12')

        post_tomorrow = mixer.blend('posts.Post',
            content='XYZ content',
            published=now + datetime.timedelta(days=1),)
        response = self.client.get(reverse('posts:detail', args=(post_tomorrow.id,)))
        self.assertTrue(logged_in) 
        assert response.status_code ==200, 'Should be callable by staff user'
        self.assertContains(response, 'XYZ content')
    def test_staff_user_with_past_and_draft_post(self):
        # create staff user
        user = User.objects.create_user(is_staff=True,
                                        username='adminuser', 
                                        # email='oo@gmail.com',
                                        password='oleKolewski12')
        # You'll need to log him in before you can send requests through the client
        logged_in = self.client.login(username='adminuser', password='oleKolewski12')

        post_tomorrow = mixer.blend('posts.Post',
            content='XYZ content',
            published=now - datetime.timedelta(days=1),
            draft=True)
        response = self.client.get(reverse('posts:detail', args=(post_tomorrow.id,)))
        self.assertTrue(logged_in) 
        assert response.status_code ==200, 'Should be callable by staff user'
        self.assertContains(response, 'XYZ content')

class TestPostDetail(TestCase):
    def test_post_detail_published_in_future(self):
        """
        A post with a published in the future should
        return a 404 not found for non-staff users.
        """
        post = mixer.blend('posts.Post',
            published=now + datetime.timedelta(days=1),)

        url = reverse('posts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestDeleteView(TestCase):
    def test_anonymous(self):
        post = mixer.blend('posts.Post')
        url = reverse('posts:delete', args=(post.id,))
        response = self.client.get(url)
        assert response.status_code == 404, 'Should generate an 404 error'

    def test_staff_user(self):
        post = mixer.blend('posts.Post')
        user = User.objects.create_user(is_staff=True,
                                        username='staffuser',
                                        password='somepassforA1')
        logged_in = self.client.login(username='staffuser', password='somepassforA1')
        url = reverse('posts:delete', args=(post.id,))
        # Use the follow=True option in the client.get()
        response = self.client.get(url, follow=True)
        expected_url = reverse('posts:home')

        # get message from context and check that expected text is there
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, 'Post deleted')

        self.assertTrue(logged_in)
        # due to follow=True redirection code is not visible, use assertRedirects
        assert response.status_code == 200, 'Should be callable by staff user'
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertFalse(Post.objects.all())

class TestUpdateView(TestCase):
    def test_anonymous(self):
        post = mixer.blend('posts.Post')
        url = reverse('posts:update', args=(post.id,))
        response = self.client.get(url)
        assert response.status_code == 404, 'Should generate an 404 error'

    def test_staff_user_get(self):
        post = mixer.blend('posts.Post')
        staff_user = User.objects.create_superuser(is_staff=True,
                                                email='oo@gm.com',
                                                username='staffuser',
                                                password='somepassforA1')
        logged_in = self.client.login(username='staffuser', password='somepassforA1')
        url = reverse('posts:update', args=(post.id,))
        response = self.client.get(url)

        self.assertTrue(logged_in)
        assert response.status_code == 200, 'Should be callable by staff user'

    def test_staff_user_post(self):
        staff_user = User.objects.create_superuser(is_staff=True,
                                                email='oo@gm.com',
                                                username='staffuser',
                                                password='somepass')
        logged_in = self.client.login(username='staffuser', password='somepass')
        category = mixer.blend('posts.Category')
        post = mixer.blend('posts.Post', content='old content')
        
        today = datetime.date.today()
        data={'content': 'new content',
            'author': staff_user.pk,
            'title': 'some title',
            'published': today,
            'read_time': 1,
            'category': [category.pk],}
        url = reverse('posts:update', args=(post.id,))
        response = self.client.post(url, data)

        self.assertTrue(staff_user.is_superuser)
        self.assertTrue(logged_in)
        # read post again from db afer saving changes
        post.refresh_from_db()
        self.assertEqual(post.content, 'new content')

        # get message from context and check that expected text is there
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, 'Post Updated')

        # test redirections:
        assert response.status_code == 302, 'Should redirect to success view'
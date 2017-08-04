import datetime
import pytest

from mixer.backend.django import mixer
from .. models import Post, create_slug
pytestmark = pytest.mark.django_db
now = datetime.datetime.now()

class TestPost():
    def test_post_create(self):
        'should create Post instance'
        post = mixer.blend('posts.Post')
        assert post.id == 1
    def test_post_str(self):
        'str method should return title of the Post instance'
        post = mixer.blend('posts.Post', title='some name')
        assert str(post) == 'some name'

class TestCategory():
    def test_category_create(self):
        'should create category instance'
        category = mixer.blend('posts.category')
        assert category.id == 1

class TestPostManager():
    def test_post_model_manager(self):
        """
        .active method provided by model manager should return filtered results
        """
        post_yesterday = mixer.blend('posts.Post',
            published=now - datetime.timedelta(days=1),)

        post_tomorrow = mixer.blend('posts.Post',
            published=now + datetime.timedelta(days=1),)

        post_yesterday_draft = mixer.blend('posts.Post',
            published=now - datetime.timedelta(days=1),
            draft=True,)

        active_posts = Post.objects.active()
        filtered_objects = Post.objects.filter(draft=False, published__lte=now)
        # two querysets are always different even when contain same info, change them to list
        assert list(active_posts) == list(filtered_objects)
        assert len(active_posts) ==1

class TestCreteSlug():
    def test_create_slug(self):
        'shoud generete a different slug'
        old_slug = 'some_slug'
        post = mixer.blend('posts.Post', slug=old_slug)
        new_slug = create_slug(post, old_slug)
        assert new_slug != old_slug
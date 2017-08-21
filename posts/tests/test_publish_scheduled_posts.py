from mixer.backend.django import mixer
import pytest
pytestmark = pytest.mark.django_db
import datetime
from .. publish_scheduled_posts import automatic_publish
from ..models import Post

class TestPublishScheduledPosts():
    def test_publish(self):
        today = datetime.datetime.today()
        post_yesterday = mixer.blend('posts.Post',
                                    content='past content 1',
                                    published=today - datetime.timedelta(days=1),
                                    draft=True)
        post_today = mixer.blend('posts.Post',
                                    content='content 2',
                                    published=today,
                                    draft=True)
        post_tomorrow = mixer.blend('posts.Post',
                                    content='past content 3',
                                    published=today + datetime.timedelta(days=1),
                                    draft=True)
        automatic_publish()

        published_and_active = Post.objects.filter(draft=False)
        assert len(published_and_active) == 1
        assert published_and_active[0].content == 'content 2'
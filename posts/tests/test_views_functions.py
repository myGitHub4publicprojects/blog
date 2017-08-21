import datetime
import pytest
from mixer.backend.django import mixer
from ..models import Post
from ..views_functions import sidebar

pytestmark = pytest.mark.django_db
class TestViewsFucntions():
    def test_sidebar(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        for i in range(6):
            mixer.blend('posts.Post', title='title %s'%i, published=yesterday)
        sidebar_context = sidebar()
        assert len(Post.objects.all()) == 6
        assert len(sidebar_context['recent_posts']) == 5, 'sidebar should have 5 active posts'
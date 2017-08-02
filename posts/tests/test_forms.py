import pytest
from .. import forms
from posts.models import Category
from mixer.backend.django import mixer
from datetime import date

pytestmark = pytest.mark.django_db


class TestPostForm():
    def test_empty_form(self):
        form = forms.PostForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is given'

    def test_not_empty_form(self):
        staff_user = mixer.blend('auth.User')
        category = mixer.blend('posts.Category')
        today = date.today()
        data={'content': 'some content',
            'author': staff_user.pk,
            'title': 'some title',
            'published': today,
            'read_time': 1,
            'category': [category.pk],}
        form = forms.PostForm(data=data)
        assert form.errors == {}, 'shoud be empty'
        assert form.is_valid() is True, 'Should be valid if data is given'
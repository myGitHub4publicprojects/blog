from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ['author', 'title', 'content', 'image', 'draft', 'published', 'category']
        exclude = ['objects', 'updated', 'timestamp', 'slug']
from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    published = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Post
        # fields = ['author', 'title', 'content', 'image', 'draft', 'published', 'category']
        exclude = ['objects', 'updated', 'timestamp', 'slug']
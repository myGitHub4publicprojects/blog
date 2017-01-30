from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
    def save(self, commit=True):
        print(self.cleaned_data)
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if k != "image" ])
        print(self.cleaned_data)
        print('mysaveworks')
        return super(PostForm, self).save(commit=commit)
import datetime
from .models import Post

def automatic_publish():
    '''
    changes draft to False on posts with published set for today, remember to set task to run daily at 00:00
    '''
    today = datetime.datetime.now().date()
    unpublished = Post.objects.filter(published=today)
    for post in unpublished:
        post.draft=False
        post.save()
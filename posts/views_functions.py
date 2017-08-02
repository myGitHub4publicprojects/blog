from django.db.models import Q

from .models import Category, Post

def sidebar():
    # recent posts in sidebar
    if len(Post.objects.active()) > 5:
        recent_posts = Post.objects.active().order_by('published')[:5]
    else:
        recent_posts = Post.objects.active().order_by('published')

    # categories in sidebar
    categories =  Category.objects.all()

    # archives links in sidebar
    archives = {}
    for x in Post.objects.active():
        date = x.published.strftime("%b%Y")
        archives[date] = archives.get(date,0) + 1

    sidebar_context = {
        'archives': archives,
        'recent_posts': recent_posts,
        'categories': categories
        }
    return sidebar_context

def queryset_filtered(qs, query):
    return qs.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__username__icontains=query)|
            Q(title__icontains=query)
        ).distinct()
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from .models import Post, upload_location
from .forms import PostForm

def home(request):
    queryset_list = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        'post_list': queryset,
    }
    return render(request, 'posts/home.html', context)

def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save_no_img()
        if request.FILES:
            instance.image = request.FILES['image']
        instance.save()
        messages.success(request, 'Post Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form
    }
    return render(request, 'posts/post_form.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'posts/post.html', context)

def update(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Post.objects.get(pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        messages.success(request, 'Post Updated')
        return HttpResponseRedirect(reverse('posts:detail', args=(instance.id,)))

    context = {
        'form': form
    }
    return render(request, 'posts/post_form.html', context)

def delete(request, pk):
    instance = Post.objects.get(pk=pk)
    instance.delete()
    messages.success(request, 'Post deleted')
    return redirect('posts:home')
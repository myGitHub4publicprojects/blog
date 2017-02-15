from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone

from .models import Category, Post
from .forms import PostForm

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

def home(request, pk=None, category=None):

    queryset_list = Post.objects.active().order_by('-published')
    if request.user.is_staff:
        queryset_list = Post.objects.all().order_by('-published')

    # search
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__username__icontains=query)|
            Q(title__icontains=query)
        ).distinct()

    # category qs
    if category:
        category_obj = Category.objects.filter(name=category)
        queryset_list = Post.objects.active().filter(category=category_obj)

    # archives qs
    if pk:
        import calendar
        month = pk[:3]
        year = pk[3:]
        months = dict((v,k) for k,v in enumerate(calendar.month_abbr))
        month_digit = months[month]
        queryset_list = Post.objects.active().filter(published__year=year, published__month=month_digit)
    
    # pagination
    items_per_page = 5
    if request.GET.get('iitems'):
        items_per_page = int(request.GET.get('iitems'))
    paginator = Paginator(queryset_list, items_per_page) # Show x number of items per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {'post_list': queryset}
    context.update(sidebar())

    return render(request, 'posts/home.html', context)

def create(request):
    if not request.user.is_staff:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save_no_img()
        if request.FILES:
            instance.image = request.FILES['image']
        instance.save()
        form.save_m2m() # for categories (many to many field) to work
        messages.success(request, 'Post Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {'form': form}

    return render(request, 'posts/post_form.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    if not request.user.is_staff:
        if post.draft or post.published > timezone.now().date():
            raise Http404
    context = {'post': post}
    context.update(sidebar())

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

    context = {'form': form}

    return render(request, 'posts/post_form.html', context)

def delete(request, pk):
    if not request.user.is_staff:
        raise Http404
    instance = Post.objects.get(pk=pk)
    instance.delete()
    messages.success(request, 'Post deleted')
    return redirect('posts:home')

def create_pdf(request, pk):
    from django.http import HttpResponse
    from reportlab.platypus.doctemplate import SimpleDocTemplate
    from reportlab.lib import styles
    from reportlab.lib.styles import getSampleStyleSheet
    from django.conf import settings
    import os
    from reportlab.platypus import (
        BaseDocTemplate, 
        PageTemplate, 
        Frame, 
        Paragraph,
        Image
            )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import (
        black,
        purple,
        white,
        yellow,
        blue
            )

    post = Post.objects.get(pk=pk)
    # Set up HttpResponse object
    response = HttpResponse(content_type='application/pdf')
    filename = post.slug
    response['Content-Disposition'] = 'attachment; filename= %s.pdf'%filename
    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    title = Paragraph(post.title, styles['Title'])

    # use custom styles
    styles= {
            'default': ParagraphStyle(
                'default',
                fontName='Times-Roman',
                fontSize=14,
                leading=12,
                leftIndent=0,
                rightIndent=0,
                firstLineIndent=0,
                alignment=TA_LEFT,
                spaceBefore=0,
                spaceAfter=0,
                bulletFontName='Times-Roman',
                bulletFontSize=10,
                bulletIndent=0,
                textColor= black,
                backColor=None,
                wordWrap=None,
                borderWidth= 0,
                borderPadding= 0,
                borderColor= None,
                borderRadius= None,
                allowWidows= 1,
                allowOrphans= 0,
                textTransform=None,  # 'uppercase' | 'lowercase' | None
                endDots=None,         
                splitLongWords=1,
            ),
        }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=purple,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=blue,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    styles['small'] = ParagraphStyle(
        'small',
        parent=styles['default'],
        leading=14,
        borderColor=black,
        borderWidth=0,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
        textColor=purple,
        fontSize=10,
    )
    styles['link'] = ParagraphStyle(
        'link',
        parent=styles['default'],
        leading=14,
        borderColor=black,
        borderWidth=0,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
        textColor=blue,
        fontSize=14,
    )

    author = post.author.username
    published = post.published
    caption = Paragraph('Published by %s | %s'%(author, published), styles['small'])
    content = Paragraph(post.content, styles['default'])
    relative_url = post.get_absolute_url()
    full_url = request.build_absolute_uri(relative_url)
    url_paragraph = Paragraph('Article from: ' + full_url, styles['alert'])
    address = '<link href="' + full_url + '">' + 'Click here to read this article online' + '</link>'
    address_paragraph = Paragraph(address, styles['link'])
    image = Image(post.image,  width=200, height=200)
    header_image = Image(os.path.join(settings.STATIC_ROOT, 'posts/img/header.jpg'),  width=600, height=100)
    
    Elements = [header_image, url_paragraph, title, caption, image, content, address_paragraph]
    doc.build(Elements)

    return response
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id: # to prevent changing slug on updates
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

def upload_location(instance, filename):
    return '%s/%s'%(instance.id, filename)

class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(draft=False, published__lte=timezone.now())

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    published = models.DateField(auto_now=False, auto_now_add=False)
    draft = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
    
    def save_no_img(self):
        self.image = None
        return super(Post, self).save()
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
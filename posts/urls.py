from django.conf.urls import url, include
from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<pk>[0-9]+)$', views.detail, name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.update, name='update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
]

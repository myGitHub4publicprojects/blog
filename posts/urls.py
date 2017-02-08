from django.conf.urls import url, include
from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<pk>[0-9]+)$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/create_pdf/$', views.create_pdf, name='create_pdf'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.update, name='update'),
    url(r'^archives/(?P<pk>[A-Z][a-z]{2}[0-9]{4})$', views.home, name='archives'),
    url(r'^category/(?P<category>.+)$', views.home, name='category'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
]

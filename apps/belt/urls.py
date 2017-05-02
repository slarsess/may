from django.conf.urls import url
# from django.contrib import admin

from . import views

app_name ='belt'
urlpatterns = [
    url(r'^index$', views.index, name ='index'),
    # url(r'^add$', views.add, name='add'),
    # url(r'^post$', views.post, name='post'),
    # url(r'^detail/(?P<id>\d+)$', views.detail, name='detail'),
    # url(r'^users/(?P<id>\d+)$', views.users, name='users'),
]

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<i>[0-9]+)/$', views.result, name='result'),
]

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<query_value.0>[0-9]+)/$', views.result, name='result'),
]

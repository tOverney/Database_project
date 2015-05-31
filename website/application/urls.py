from django.conf.urls import include, url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<query_index>[0-9]+)/$', views.result, name='result'),
] + staticfiles_urlpatterns()

from django.conf.urls import include, url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<query_index>[0-9]+)/$', views.result, name='result'),
    url(r'^search_res/$', views.search_result, name='search_result'),
    url(r'^followup/(?P<selected>[a-zA-Z]+)/(?P<id>[0-9]+)/$',
        views.followup, name='followup search'),
    url(r'^dispatching_page/$', views.dispatching_page, name='dispatcher')
] + staticfiles_urlpatterns()

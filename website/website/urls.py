from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', include('application.urls')),
    # url(r'^blog/', include('blog.urls')),
]

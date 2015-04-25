from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', include('application.urls')),
    # url(r'^blog/', include('blog.urls')),
]

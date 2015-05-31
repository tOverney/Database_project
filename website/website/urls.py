from django.conf.urls import include, url

urlpatterns = [
    url(r'^application/', include('application.urls')),
]

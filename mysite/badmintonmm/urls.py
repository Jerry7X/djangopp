from django.conf.urls import include, url
from badmintonmm.views import index, deposit


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^deposit/$', deposit), 
]

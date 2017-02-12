from django.conf.urls import include, url
from badmintonmm.views import *


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^manage/$', index),
    url(r'^deposit/$', deposit), 
    url(r'^addball/$', addball),
    url(r'^play/$', play),
]


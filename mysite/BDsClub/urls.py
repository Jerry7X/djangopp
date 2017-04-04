from django.conf.urls import include, url
from BDsClub.views import *


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^home/$', bdsclub),
    url(r'^deposit/$', deposit), 
    url(r'^addball/$', addball),
    url(r'^playall/$', playall),
    url(r'^apply/$', apply),
]


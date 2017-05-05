from django.conf.urls import include, url
from BDsClub.views import *


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^home/$', bdsclub),
    url(r'^deposit/$', deposit), 
    url(r'^addball/$', addball),
    url(r'^playall/$', playall),
    url(r'^apply/$', apply),
    url(r'^get_yue', wx_my_amount),
    url(r'^wx_get_curplay', wx_get_curplay),
    url(r'^wx_apply', wx_apply),
    url(r'^wx_get_fee_history', wx_get_fee_history),
    url(r'^wx_get_play_history', wx_get_play_history),
    url(r'^alias/$', alias),
]


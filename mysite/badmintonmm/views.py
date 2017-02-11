from django.http import HttpResponse
from django.shortcuts import render
from badmintonmm.models import Deposit
from datetime import *
import pytz
 
def index(request):
    rets = list(Deposit.objects.all())
    #results = []
    #for ret in rets:
    #    results.append({'name': ret[0],'amount':ret[1],'time':ret[2]})
    return render(request, 'totalcount.html',{'results': rets})
    #return HttpResponse(str(rets[0].name))

def deposit(request):
    dp = Deposit()
    dp.name = request.GET['name']
    dp.amount = request.GET['amount']
    tz = pytz.timezone(pytz.country_timezones('cn')[0])
    dp.time = datetime.now(tz)
    dp.save()
    return index(request)

from django.http import HttpResponse
from django.shortcuts import render
from badmintonmm.models import *
import pytz
import datetime
 
def get_total():
    rets = list(TotalCount.objects.all())
    return rets[0]

def index(request):
    return render(request, 'play.html')
    
def home(request):
    rets = list(Deposit.objects.all())
    membercounts = list(MemberCount.objects.all())
    total = get_total()
    balls = list(Ball.objects.all())
    plays = list(PlayOne.objects.all())
    #results = []
    #for ret in rets:
    #    results.append({'name': ret[0],'amount':ret[1],'time':ret[2]})
    return render(request, 'totalcount.html',{'results': rets,'members': membercounts,
                     'total':total,'balls':balls,'plays':plays})
    #return HttpResponse(str(rets[0].name))

def deposit(request):
    dp = Deposit()
    dp.name = request.GET['name']
    dp.amount = float(request.GET['amount'])
    tz = pytz.timezone(pytz.country_timezones('cn')[0])
    dp.time = datetime.date.today()
    mc,created = MemberCount.objects.get_or_create(name=dp.name)
    #mc.name = dp.name
    if not created:
        mc = MemberCount.objects.get(name=dp.name)
        print(mc.t_amount)
        print(type(dp.amount))
        mc.t_amount = mc.t_amount + dp.amount
        mc.l_amount = mc.l_amount + dp.amount
    else:
        mc.t_amount = dp.amount
        mc.l_amount = dp.amount

    total = get_total()
    total.total = total.total + dp.amount
    total.left = total.left + dp.amount
    dp.save()
    mc.save()
    total.save()
    return index(request)

def addball(request):
    bl = Ball()
    bl.name = request.GET['name']
    bl.count = int(request.GET['count'])
    bl.l_count = bl.count
    bl.price = request.GET['price']
    bl.save()
    return index(request)

def play(request):
    po = PlayOne()
    po.time = datetime.date.today()
    po.players = request.GET['players']
    po.place = request.GET['place']
    po.duration = int(request.GET['duration'])
    po.fee = float(request.GET['fee'])
    po.ballused = int(request.GET['ballused'])
    po.balltype = request.GET['balltype']
    #check player
    players = po.players.split(';')
    for player in players:
        try :
            member = MemberCount.objects.get(name=player)
        except ObjectDoesNotExist:
            return HttpResponse("no this member" + player)
    
    totalfee = 0.0
    try :
        ball = Ball.objects.get(name=po.balltype)
        totalfee = po.fee + ball.price * po.ballused
        po.aaprice = totalfee / len(players)
        # reduce left ball
        ball.l_count = ball.l_count - po.ballused
        ball.save()
    except ObjectDoesNotExist:
        return HttpResponse("no this ball type")
   
    po.save()
    # reduce member left amount
    for player in players:
        member = MemberCount.objects.get(name=player)
        member.l_amount = member.l_amount - po.aaprice
        member.save()

    #calc total
    total = get_total()
    total.left = total.left - totalfee
    total.save()
    return index(request)

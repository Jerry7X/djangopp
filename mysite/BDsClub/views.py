from django.http import HttpResponse
from django.shortcuts import render
from BDsClub.models import *
from django.core import serializers
import json
import datetime
 
def bdsclub(request):
    play = get_current_play()
    players = get_current_players(play.id)
    return render(request, 'play1.html', {'players':players, 'play': play})
    
def home(request):
    rets = list(Deposit.objects.all().order_by('-time'))
    member = list(Member.objects.all())
    als = list(Alias.objects.all())
    balls = list(Ball.objects.all())
    plays = list(Play.objects.all().order_by('-time'))
    for play in plays:
        play.players = get_current_players(play.id)
    return render(request, 'summary.html',{'results': rets,'members': member,
                     'als':als,'balls':balls,'plays':plays})

def wx_get_fee_history(request):
    feehis = []
    dt = 0.0
    ct = 0.0
    mname = get_realname(request.GET['name'])
    if mname is None:
        res = { 'dt': dt, 'ct': ct, 'feelist': feehis }
        return HttpResponse(json.dumps(res))

    rets = list(Deposit.objects.filter(name = mname).order_by('-time'))
    for ret in rets:
        if ret.amount > 0:
            dt = dt + ret.amount
        else:
            ct = ct + ret.amount
        feehis.append({'time': str(ret.time), 'amount': ret.amount })
    res = { 'dt': dt, 'ct': ct, 'feelist': feehis }
    return HttpResponse(json.dumps(res))

def get_realname(name):
    try:
       al = Alias.objects.get(wx_name = name)
       rname = al.real_name
       if rname == 'None' :
           rname = None
    except Alias.DoesNotExist:
       al = Alias()
       al.real_name = 'None'
       al.wx_name = name
       al.save()
       rname = None
    return rname

def wx_get_play_history(request):
    mname = get_realname(request.GET['name'])
    apply_list = []
    if mname is None :
        return HttpResponse(json.dumps(apply_list))

    aps = list(Apply.objects.filter(name = mname).order_by('-pid'))
    for ap in aps:
        players = get_current_players(ap.pid)
        play = Play.objects.get(id = ap.pid)
        apply_list.append({'id': ap.pid, 'time': play.play_time, 'players': players})
    return HttpResponse(json.dumps(apply_list))

def wx_get_current_players(ppid):
    players = Apply.objects.filter(pid = ppid)
    pls = ''
    #lines = 0
    num = 1
    for player in players:
         #if (len(pls) - lines * 20) > 20:
         pls = pls + str(num) + ')'+ player.name + '   '
         #if num % 3 == 0 :
         #lines = lines + 1
         pls = pls + '\n'
         num = num + 1
    return pls

def wx_get_curplay(request):
    play = get_current_play()
    players = wx_get_current_players(play.id)
    no_apply = True
    if play.state == 1:
        no_apply = False
    res = {"id": play.id, "place": play.place, "duration": play.duration + '\n', "players": players, "state": no_apply }
    return HttpResponse(json.dumps(res))

def check_member(mname, amount):
    mc,created = Member.objects.get_or_create(name=mname)
    if not created:
        if amount != 0 :
            mc = Member.objects.get(name=mname)
            mc.amount = mc.amount + amount
            mc.save()
    else:
        mc.amount = amount
        mc.save()

def deposit_fun(name, amount):
    dp = Deposit()
    dp.name = name
    dp.amount = amount
    dp.time = datetime.date.today()
    check_member(dp.name, dp.amount);
    dp.save()


def deposit(request):
    try:
       al = Alias.objects.get(real_name = request.GET['name'])
    except Alias.DoesNotExist:
       return render(request, 'error.html',{'error': "do not deposit for no register user!!!"})
    deposit_fun(request.GET['name'], float(request.GET['amount']))
    return home(request)

def alias(request):
    al = Alias()
    al,created = Alias.objects.get_or_create(wx_name = request.GET['wxname'])
    al.real_name = request.GET['name']
    al.wx_name = request.GET['wxname']
    al.save()
    return home(request)

def wx_my_amount(request):
    mname = get_realname(request.GET['name'])
    if mname is None :
       #remember user wx name
       res = {"amount": 0.0 }
       return HttpResponse(json.dumps(res))

    mc,created = Member.objects.get_or_create(name=mname)
    res = {"amount": round(mc.amount) }
    #json_data = serializers.serialize("json", mc)
    return HttpResponse(json.dumps(res))
        

def addball(request):
    bl = Ball()
    bl.name = request.GET['name']
    bl.price = request.GET['price']
    bl.save()
    return home(request)

def get_current_play():
    plays = list(Play.objects.all().order_by('-id'))
    if not plays:
        py = Play()
        py.id = 0
        return py
    else:
        return plays[0]

def get_current_players(ppid):
    players = Apply.objects.filter(pid = ppid)
    pls = ''
    for player in players:
         pls = pls + player.name + ';'
    return pls

# list plays which member join in
def get_play_history(request):
    # todo
    return home(request)

def play_start(request):
    py = get_current_play()
    if py.id != 0 and py.state != 3 and py.state != 4 :
        return render(request, 'error.html',{'error': "last play not end!!!"})
    pn = Play()
    pn.id = py.id + 1
    pn.time = datetime.date.today()
    pn.play_time = request.GET['play_time']
    pn.place = request.GET['place']
    pn.duration = request.GET['duration']
    pn.fee = 0
    pn.aaprice = 0
    pn.state = 1
    pn.save()
    return home(request)

def play_running(request):
    py = get_current_play()
    if py.state != 1 :
        return render(request, 'error.html',{'error': "play not start!!!"})
#update place and time
    players = Apply.objects.filter(pid = py.id)
    if (len(players) == 0) :
        return render(request, 'error.html',{'error': "no players, you should run the play!!!"})

    py.place = request.GET['place']
    py.duration = request.GET['duration']
    py.state = 2
    py.save()
    return home(request)

def apply(request):
    py = get_current_play()
    if py.state != 1 :
        return render(request, 'error.html',{'error': "it is going on,can not join now!!!"})
    # check whether member apply or not
    
    num, affected = Apply.objects.filter(name = request.GET['name'], pid = py.id).delete()
    print(num)
    if num == 0 : 
        ap = Apply()
        ap.name = request.GET['name']
        ap.pid = py.id
        # here do
        check_member(ap.name, 0)        
        ap.save()
    return home(request)

def wx_apply(request):
    py = get_current_play()
    if py.state != 1 :
        res = {"result": -1}
        return HttpResponse(json.dumps(res))
    rname = get_realname(request.GET['name'])
    if rname is None:
        res = {"result": -2}
        return HttpResponse(json.dumps(res))

    num, affected = Apply.objects.filter(name = rname, pid = py.id).delete()
    print(num)
    if num == 0 :
        ap = Apply()
        ap.name = rname
        ap.pid = py.id
        # here do
        check_member(ap.name, 0)
        ap.save()
        res = {"result": 0}
    else :
        res = {"result": 1}

    return HttpResponse(json.dumps(res))
    
def play_cancel(request):
    py = get_current_play()
    #if py.state != 1 :
    #    return render(request, 'error.html',{'error': "can not cancel!!!"})

    #if py.state == 1 :
    py.state = 4
    py.save()

    return home(request)

def play_end(request):
    py = get_current_play()
    if py.state != 2 :
        return render(request, 'error.html',{'error': "play not running!!!"})

    py.fee = float(request.GET['fee'])
    py.fee_comment = request.GET['comment']

    #check player
    players = Apply.objects.filter(pid = py.id)
    if (len(players) == 0) :
        return render(request, 'error.html',{'error': "no players, you should cancel the play!!!"})
    py.aaprice = round(py.fee / len(players), 3)
    # end
    py.state = 3
    py.save()
    
    # reduce member left amount
    for player in players:
        deposit_fun(player.name, -py.aaprice)

    return home(request)

def playall(request):
    if request.GET.has_key("start"):
        return play_start(request)
    if request.GET.has_key("running"):
        return play_running(request)
    if request.GET.has_key("cancel"):
        return play_cancel(request)
    if request.GET.has_key("end"):
        return play_end(request)
    print("no key")
    return home(request)

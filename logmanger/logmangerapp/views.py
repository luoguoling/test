from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import socket
from django.db import connection,models
from logmangerapp.models import AddLogpath
from logmangerapp.models import AddPhpLogpath
from logmangerapp.models import addCommand
import MySQLdb
import json,urllib
import logging
from django.http import HttpResponse
from mysql import db_operate
from selectip import select_ip
from selectPlatformAlias import select_platformAlias
from logmanger import settings
from django.contrib.auth import authenticate,login
from logmangerapp.forms import LoginForm
# Create your views here.
def socket_send(ip,command):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,1003))
    sock.send(command)
    data = ""
    count = 1
    End = "#zbcyh#"
    total_data = []
    while True:
        data = sock.recv(8192)
        count = count + 1
        print count
        if not len(data):
            break
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    recv_data = ''.join(total_data)
    sock.close()
    return recv_data
@csrf_exempt
def view(request):
    return render_to_response('test4.html')
@csrf_exempt
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html',RequestContext(request,{'form':form}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            response = HttpResponseRedirect('view')
            response.set_cookie('username',username,max_age=3600)
            if user is not None and user.is_active:
                auth.login(request,user)
                return render_to_response('test4.html',{'form':form,'password_is_wrong':True})
            else:
                return render_to_response('login.html',{'form':form,'password_is_wrong':True})
        else:
            return render_to_response('login.html',{'form':form,})

@csrf_exempt
def view2(request):
    """check php log"""
    logpathlist = AddPhpLogpath.objects.all()
    print 'the path is %s',logpathlist
    sql2 = 'select distinct(platformAlias) from mds_server'
    db = db_operate()
    platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    print platformAliass
    try:
        log = logging.getLogger('test1')
        log.info('log content')
    except:
        print 'no log'
    TxtlogResult = ['ceshi','ceshi2']
    if request.method=='POST':
        try:
	    logTime=request.POST['date']
	except:
	    pass
        try:
	    platformAlias=request.POST['agent']
	except:
	    pass
        try:
	    logPath=request.POST['logdir']
	except:
	    pass
	try:
	    serverId=request.POST['zone']
	except:
	    pass
	try:
	    logCount=request.POST['sum']
	except:
	    pass
	print logTime,platformAlias,logPath,serverId,logCount
        A = select_ip()
        serverIp = A.selectip(platformAlias,serverId)
        print 'serverIp is %s' %(serverIp)
	logexist = AddPhpLogpath.objects.all()
        print logexist
	for list in logexist:
	    print list.logpath
	if list.logpath == logPath:
	    print 'the logpath is exist'
	else:
	    l1 = AddPhpLogpath(logpath=logPath)
	    l1.save()
        serverinfo_list = []
        serverinfo = {}
        serverinfo["platformAlias"] = platformAlias
        serverinfo["serverId"] = serverId
        serverinfo["serverIp"] = serverIp
        serverinfo["logPath"] = logPath
        serverinfo["logTime"] = logTime
        serverinfo["logCount"] = logCount
        serverinfo_list.append(serverinfo)
        command = {}
        command["cmd"] = 'logoperate'
        command["checkType"] = 'phplog'
        command["serverinfo_list"] = serverinfo_list
        command = json.dumps(command) + "#zbcyh#"
        print command
        try:
            logResult = socket_send('14.18.204.150',command)
        except:
            print 'not connect'
        JsLogResult = json.loads(logResult)
        TxtlogResult = JsLogResult['msg']
        print TxtlogResult
    return render_to_response('logquery3.html',{'result':logpathlist,'result2':platformAliass,'result3':TxtlogResult})
@csrf_exempt
def checkjavalog(request):
    """serach java log"""
    logpathlist = AddLogpath.objects.all()
    print 'the path is %s',logpathlist
    sql2 = 'select distinct(platformAlias) from mds_server'
    db = db_operate()
    platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    TxtlogResult = ['ceshi','ceshi2']
    key = ""
    if request.method=='POST':
        try:
	    logTime=request.POST['date']
	except:
	    pass
        try:
	    platformAlias=request.POST['agent']
	except:
	    pass
        try:
	    logPath=request.POST['logdir']
	except:
	    pass
	try:
	    serverId=request.POST['zone']
	except:
	    pass
        try:
            key=request.POST['key']
        except:
            pass
        try:
            hour=request.POST['hour']
        except:
            pass
	print logTime,platformAlias,logPath,serverId,hour
	sql = 'select serverIp from mds_server where platformAlias="%s" and serverId="%s"' %(platformAlias,serverId)
        serverIp1 = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        for serverIp in serverIp1:
	    print serverIp
            """
	logexist = AddLogpath.objects.all()
        print logexist
	for list in logexist:
	    print list.logpath
	if list.logpath == logPath:
	    print 'the logpath is exist'
	else:
	    l1 = AddLogpath(logpath=logPath)
	    l1.save()
        """
        queryset = AddLogpath.objects.values('logtype').filter(logpath=logPath)[0]['logtype']
        print 'the querysettype is'
        print queryset
        serverinfo_list = []
        serverinfo = {}
        serverinfo["platformAlias"] = platformAlias
        serverinfo["serverId"] = serverId
        serverinfo["serverIp"] = serverIp
        serverinfo["logPath"] = logPath
        serverinfo["logTime"] = logTime
        serverinfo["key"] = key
        serverinfo['logtype'] = queryset
        serverinfo['hour'] = hour
        serverinfo_list.append(serverinfo)
        command = {}
        command["cmd"] = 'logoperate'
        command["checkType"] = 'javasearchlog'
        command["serverinfo_list"] = serverinfo_list
        print command
        command = json.dumps(command) + "#zbcyh#"
        print command
        try:
            logResult = socket_send('14.18.204.150',command)
        except:
            print 'not connect'
        try:
            JsLogResult = json.loads(logResult)
            TxtlogResult = JsLogResult['msg']
        except:
            print 'not value'
        print TxtlogResult
    return render_to_response('checkjavalog.html',{'result':logpathlist,'result2':platformAliass,'result3':TxtlogResult})
@csrf_exempt
def downjavalog(request):
    """download java log"""
    logpathlist = AddLogpath.objects.all()
    print 'the path is %s',logpathlist
    sql2 = 'select distinct(platformAlias) from mds_server'
    db = db_operate()
    platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    TxtlogResult = ['ceshi','ceshi2']
    if request.method=='POST':
        try:
	    logTime=request.POST['date']
	except:
	    pass
        try:
	    platformAlias=request.POST['agent']
	except:
	    pass
        try:
	    logPath=request.POST['logdir']
	except:
	    pass
	try:
	    serverId=request.POST['zone']
	except:
	    pass
        try:
            hour = request.POST['hour']
        except:
            pass
	print logTime,platformAlias,logPath,serverId,hour
	sql = 'select serverIp from mds_server where platformAlias="%s" and serverId="%s"' %(platformAlias,serverId)
        serverIp1 = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        print serverIp1
        for serverIp in serverIp1:
	    print serverIp
            """
	logexist = AddLogpath.objects.all()
        print logexist
	for list in logexist:
	    print list.logpath
	if list.logpath == logPath:
	    print 'the logpath is exist'
	else:
	    l1 = AddLogpath(logpath=logPath)
	    l1.save()
            """
        queryset = AddLogpath.objects.values('logtype').filter(logpath=logPath)[0]['logtype']
        print queryset
        serverinfo_list = []
        serverinfo = {}
        serverinfo["platformAlias"] = platformAlias
        serverinfo["serverId"] = serverId
        serverinfo["serverIp"] = serverIp
        serverinfo["logPath"] = logPath
        serverinfo["logTime"] = logTime
        serverinfo["hour"] = hour
        serverinfo['logtype'] = queryset
        serverinfo_list.append(serverinfo)
        command = {}
        command["cmd"] = 'logoperate'
        command["checkType"] = 'downjavalog'
        command["serverinfo_list"] = serverinfo_list
        command = json.dumps(command) + "#zbcyh#"
        print command
        try:
            logResult = socket_send('14.18.204.150',command)
        except:
            print 'not connect'
        JsLogResult = json.loads(logResult)
        TxtlogResult = JsLogResult['msg']
        print TxtlogResult
    return render_to_response('downjavalog.html',{'result':logpathlist,'result2':platformAliass})
@csrf_exempt
def searchjavalog(request):
    """check java log"""
    logpathlist = AddLogpath.objects.all()
    print 'the path is %s',logpathlist
    sql2 = 'select distinct(platformAlias) from mds_server'
    db = db_operate()
    platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    TxtlogResult = ['ceshi','ceshi2']
    if request.method=='POST':
        try:
	    logTime=request.POST['date']
	except:
	    pass
        try:
	    platformAlias=request.POST['agent']
	except:
	    pass
        try:
	    logPath=request.POST['logdir']
	except:
	    pass
	try:
	    serverId=request.POST['zone']
	except:
	    pass
        try:
            logAccount = request.POST['sum']
        except:
            pass
#	try:
#	    key=request.POST['key']
#	except:
#	    pass
#        try:
#            hour = request.POST['hour']
#        except:
#            pass
	print logTime,platformAlias,logPath,serverId,logAccount
	sql = 'select serverIp from mds_server where platformAlias="%s" and serverId="%s"' %(platformAlias,serverId)
        serverIp1 = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        print serverIp1
        for serverIp in serverIp1:
	    print serverIp
            """
	logexist = AddLogpath.objects.all()
        print logexist
	for list in logexist:
	    print list.logpath
	if list.logpath == logPath:
	    print 'the logpath is exist'
	else:
	    l1 = AddLogpath(logpath=logPath)
	    l1.save()
            """
        queryset = AddLogpath.objects.values('logtype').filter(logpath=logPath)[0]['logtype']
        print queryset
        serverinfo_list = []
        serverinfo = {}
        serverinfo["platformAlias"] = platformAlias
        serverinfo["serverId"] = serverId
        serverinfo["serverIp"] = serverIp
        serverinfo["logPath"] = logPath
        serverinfo["logTime"] = logTime
#        serverinfo["key"] = key
#        serverinfo["hour"] = hour
        serverinfo['logAccount'] = logAccount
        serverinfo['logtype'] = queryset
#        serverinfo = json.dumps(serverinfo)
        serverinfo_list.append(serverinfo)
#        serverinfo_dic = {}
#        serverinfo_dic['serverinfo'] = serverinfo_list
        command = {}
        command["cmd"] = 'logoperate'
        command["checkType"] = 'checkjavalog'
        command["serverinfo_list"] = serverinfo_list
        command = json.dumps(command) + "#zbcyh#"
        print command
        try:
            logResult = socket_send('14.18.204.150',command)
        except:
            print 'not connect'
        JsLogResult = json.loads(logResult)
        TxtlogResult = JsLogResult['msg']
        print TxtlogResult
    return render_to_response('javalogquery.html',{'result':logpathlist,'result2':platformAliass,'result3':TxtlogResult})
@csrf_exempt
def test(request):
    """add java logpath"""
    response_data = {}  
#    response_data['result'] = 'ok'  
    response_data['data'] = request.POST['url']
    response_data['data1'] = request.POST['type']
    print request.POST['url']
    print request.POST['type']
    logexist = AddLogpath.objects.all()
#    print logexist
    for list in logexist:
	print list.logpath
    if request.POST['url'] in list.logpath:
	print 'the logpath is exist'
    else:
	l1 = AddLogpath(logpath=request.POST['url'],logtype=request.POST['type'])
	l1.save()
    result = "chenggong"
#    return HttpResponse('result')
    print response_data['data']
    return HttpResponse(json.dumps(response_data['data']), content_type="application/json")
@csrf_exempt
def ExecCommand(request):
    """Exec command"""
#    P = select_platformAlias()
#    platformAliass = P.selectplatformAlias()
#    for platformAlias in platformAliass:
#        print platformAlias
    TxtCommandResult = ['result']
    execcommand = addCommand.objects.all().distinct()
#    for execcommand in execcommand1:
#        print execcommand
#    print execcommand1
   # print 'the path is %s', % execcommand1
#    for execcommand in execcommand1:
#        print 'the result is'
#        print execcommand
#        print execcommand.addcommand
    sql2='select distinct(platformAlias) from mds_server'
    db = db_operate()
    platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql2)
    print platformAliass
    if request.method == 'POST':
        try:
            platformAlias = request.POST['agent']
        except:
            pass
        try:
            serverId = request.POST['zone']
        except:
            pass
        try:
            execCommand1 = request.POST['execcommand']
            print execCommand1
            execCommand = urllib.unquote(execCommand1)
            print 'execCommand'
            print execCommand
        except:
            pass
        try:
            javapid = request.POST['javapid']
        except:
            pass
        print platformAlias,serverId,execCommand,javapid
        A = select_ip()
        serverIp = A.selectip(platformAlias,serverId)
        print serverIp
#        execcommand = ExecCommand.objects.all()
#        print execcommand
        for list in execcommand:
            print list.addcommand
        if execCommand in list.addcommand:
            print 'the command is exist'
        else:
            l2 = addCommand(addcommand=execCommand)
            l2.save()
        serverinfo_list = []
        serverinfo = {}
        serverinfo["platformAlias"] = platformAlias
        serverinfo["serverId"] = serverId
        serverinfo["serverIp"] = serverIp
        serverinfo["execcommand"] = execCommand
        serverinfo["javapid"] = javapid
        serverinfo_list.append(serverinfo)
        command = {}
        command["cmd"] = 'logoperate'
        command["checkType"] = 'ExecCommand'
        command["serverinfo_list"] = serverinfo_list
        command = json.dumps(command) + "#zbcyh#"
        print command
        try:
            commandResult = socket_send('14.18.204.150',command)
        except:
            print 'not connect'
        JsCommandResult = json.loads(commandResult)
        TxtCommandResult = JsCommandResult['msg']
        print TxtCommandResult
    return render_to_response('CommandResult.html',{'result':platformAliass,'result2':execcommand,'result3':TxtCommandResult})


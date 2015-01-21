#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from updateapp.models import serverlist
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def JSONGetView(request):
    tree_list = []
    tree_data = {}
    servers = serverlist.objects.values('id','agent','serverId','ipaddress').order_by('serverId')
    agents = serverlist.objects.values('agent').distinct().order_by('agent')
#    print type(agents)
#    print len(agents)
    agentPid = {}
    id = {}
    offset = 10000
    tree_list = []

    for i,agent in enumerate(agents):
#        print i,agent['agent']
        id[agent['agent']] = offset + i
    for key,value in id.items():
        serveragent = {}
        serveragent['serverId'] = key
        serveragent['id'] = value
        serveragent['agent'] = 'noagent'
        if serveragent not in tree_list:
            tree_list.append(serveragent)
    for server in servers:
        for key,value in id.items():
            if server['agent'] == key:
                server['parentId'] = value
                if server not in tree_list:
                    tree_list.append(server)
    #                print tree_list
#    print tree_list

        
    tree_list1 = [{'serverId': '中国', 'ipaddress': u'192.168.1.1', 'agent': u'37wan','parentId':0,"id":1},{'serverId':2L,'ipaddress':u'192.168.3.3','agent':u'中国','parentId':1,'id':7},{'serverId': 2L, 'ipaddress': u'192.168.1.2', 'agent': u'6711','parentId':0,'id':2},{'serverId': 1L, 'ipaddress': u'192.168.2.1', 'agent': u'1','parentId':2,'id':3},{'serverId':2L,'ipaddress':u'192.168.2.2','agent':u'2','parentId':2,'id':4}]
#    print tree_list
    result = json.dumps(tree_list)
#    print result
    return HttpResponse(result,content_type="application/json")
@csrf_exempt
def JSONSetView(request):
    response_data = {}
    json_tree = request.POST.get('jsonTree')
    tree_change_nodes = json.loads(json_tree)
    tree_list = []
    for i in tree_change_nodes[1:]:
        newdic = {}
        for n in i.keys():
            if 'noagent' not in i['agent']:
                newdic['agent'] = i['agent']
                newdic['zone'] = i['serverId']
                if newdic not in tree_list:
                    tree_list.append(newdic)
#    print tree_list
    for tt in tree_list:
#        print tt
        ip = serverlist.objects.values('ipaddress').filter(agent=tt['agent'],serverId=tt['zone'])
        print ip
    return HttpResponse(ip,content_type="application/json")
def ViewZtree(request):
    return render_to_response('checkbox.html')
@csrf_exempt
def updatejava(request):
    response_data = {}
#    json_tree = json.dumps([{"jsonTree":"z"}])

    json_tree = request.POST.get('jsonTree')
#    json_tree = json.dumps([{"jsonTree":"192.168.1.1"}])

    print json_tree
    try:
        tree_change_nodes = json.loads(json_tree)
        print tree_change_nodes
    
        tree_list = []
        for i in tree_change_nodes[1:]:
            newdic = {}
            for n in i.keys():
                if 'noagent' not in i['agent']:
                    newdic['agent'] = i['agent']
                    newdic['zone'] = i['serverId']
                    if newdic not in tree_list:
                        tree_list.append(newdic)
        print tree_list
        for tt in tree_list:
            print tt
            ip = serverlist.objects.values('ipaddress').filter(agent=tt['agent'],serverId=tt['zone'])
            print ip
    except:
        pass
    return render_to_response('updatejava.html')

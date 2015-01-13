from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from ztree.models import serverlist
import json
# Create your views here.
def JSONGetView(request):
    tree_list = []
    tree_data = {}
    """
    serveragent = serverlist.objects.values('agent').distinct()
    for agent1 in serveragent:
        tree_data = {}
        agent = agent1['agent']
        print agent
        print type(agent)
        tree_data['agent'] = agent
        if tree_data not in tree_list:
            tree_list.append(tree_data)
        """
        
    servers = serverlist.objects.values('agent','serverId')
    print servers
    
    for server in servers:
        print server
        server['parentId'] = 0
        server['id'] = 1
        tree_list.append(server)
    """
    tree_data['pId'] = server['agent']
    tree_data['id'] = server['serverId']
    tree_data['name'] = server['serverId']
    tree_data['open'] = "true"
    """
    #tree_data = server
    #print tree_data
       # tree_list.append(server)

    '''
    tree_data = {}
    for server in servers:
        tree_data["agent"] = server.agent
        tree_data["serverid"] = server.serverId
        print tree_data
    if tree_data not in tree_list:
        tree_list.append(tree_data)
        print tree_list
#    agent = server['agent']
    '''
    """
    print agent
    for agent in server:
        if agent not in tree_list:
            tree_list.append(agent)
    result = tree_list
    """
    tree_list1 = [{'serverId': 1L, 'ipaddress': u'192.168.1.1', 'agent': u'37wan','parentId':0,"id":1}, {'serverId': 2L, 'ipaddress': u'192.168.1.2', 'agent': u'6711','parentId':0,'id':2}, {'serverId': 1L, 'ipaddress': u'192.168.2.1', 'agent': u'1','parentId':2,'id':3},{'serverId':2L,'ipaddress':u'192.168.2.2','agent':u'2','parentId':2,'id':4}]
    print tree_list
    result = json.dumps(tree_list1)
    print result
    return HttpResponse(result,content_type="application/json")





def JSONSetView(request):
    json_tree = request.POST.get("jsonTree")
    print json_tree
    tree_change_nodes = json.loads(json_tree)
    print tree_change_nodes
    return HttpResponse(tree_change_nodes,content_type="application/json")


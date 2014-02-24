#!/usr/bin/python
file1 = open('/root/pybase/a.txt','r')
#file1 = file('a.txt')
c = file1.readlines()
dic = {}
for i in c:
	a = i.strip().split('.')
#	print a
#	print a[0]
	if a[0] + '.' + a[1] in dic.keys():
		key = dic["%s.%s" % (a[0],a[1])]
#		print key
		print key.items()
	else:
		key = []
	key.append(a[2])
	dic[a[0] + '.' + a[1]] = sorted(key)
for x,y in dic.items():
#	print x,y
	if y[0] == y[-1]:
		print '%s.%s' %(x,y[0])
	else:
		print '%s.%s-%s.%s' %(x,y[0],x,y[-1])
	

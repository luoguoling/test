#/usr/bin/python
def sum(x,y):
	
	yield x + y
for i in sum(2,3):
	print i

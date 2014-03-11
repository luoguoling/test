#!/usr/bin/python
#author:rolin
#2014-03-10
from multiprocessing import Process
def f(name):
	print name
user = ['a','b','c','d']
process_lists = []
if __name__ == "__main__":
	for i,j in enumerate(user):

		p = Process(target=f,args=(j,))
		p.start()
		
		process_lists.append(p)
for k in process_lists:
	k.join()

#!/usr/bin/python
import Queue
import threading
import time
exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        print 'qqq'
        process_data(self.name, self.q)
        print "abc"
        print "Exiting " + self.name + '\r\n'
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
            print 'me'
        time.sleep(1)
        print 'zyj'
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1
# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
# Fill the queue
print 'mmm'
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()
print 'ghi'

# Wait for queue to empty
while not workQueue.empty():
    pass
print 'yyy'
# Notify threads it's time to exit
exitFlag = 1
print 'zzzz'
# Wait for all threads to complete
for t in threads:
    t.join()
    print 'kkk'
print "Exiting Main Thread"


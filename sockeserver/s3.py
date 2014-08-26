__author__ = 'Administrator'
# -*- coding: utf-8 -*-
from SocketServer import TCPServer,ThreadingMixIn,StreamRequestHandler
import time,os,commands
#HOST = '207.198.106.114'
HOST = '211.237.12.2'
PORT = 1004
def transfertime(ret):
    a = filter(str.isdigit,ret)
    a = list(a)
    c = ''
    for i in range(len(a)):
        c += a[i]
        if i in (3,5):
            c += '-'
        if i==7:
            c += ' '
        if i in (9,11):
            c += ':'
    a = time.mktime(time.strptime(c,'%Y-%m-%d %H:%M:%S'))
    return a
def stopjava():
    os.popen('pkill java')
def startjava():
    os.popen("cd /data/game/pubserver/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd /data/game/kuafu/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
#    os.popen('cd /data/game/version/qmrserver1/qmrserver && /bin/sh start.sh')
    os.popen("cd /data/game/qmrserver_lianfu_10000/qmrserver && /bin/sh start.sh 2>&1")
    os.popen("cd /data/game/qmrserver10/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd /data/game/qmrserver20/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd /data/game/qmrserver30/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd /data/game/qmrserver40/qmrserver && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd /data/game/newversion && /bin/sh start.sh >/dev/null 2>&1")
#    os.popen("cd /data/game/huodong && /bin/sh start.sh >/dev/null 2>&1")


def updatejava():
    os.popen('rsync -vzrtopg --progress --stats  /var/ftp/qmrserver/* /data/game/newversion > /dev/null 2>&1')
logfile = open('name1.txt','a')
def log(msg):
    datenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    logstr = '%s : %s \n' %(datenow, msg)
    #print(logstr)
    logfile.write(logstr)

class Server(ThreadingMixIn,TCPServer):
    pass
class ThreadingServer(ThreadingMixIn,TCPServer):
    allow_reuse_address = True
class Handler(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                ip = self.client_address[0]
#                print ip
                ret = self.request.recv(2048).strip()
		print ret
                if ip == '221.237.152.208' or ip == '221.237.152.108' or ip == '127.0.0.1' or ip == '125.71.211.205':
                    if ret == 'reboot':
                        self.request.send('请求收到，成功处理.....')
                        stopjava()
                        time.sleep(25)
                        startjava()
                    elif ret == 'banben':
                        self.request.send('请求收到，成功处理')
                        updatejava()
                    elif ret == 'time':
                        shijian = os.popen('date +"%Y-%m-%d %H:%M:%S"').read()
                        self.request.send(shijian)
                    elif not ret:
#                        print '没有数据'
                        break
                    else:
                        self.request.send('请求收到，成功处理....')
                        try:
                            global time1
                            time1 = transfertime(ret)
                            timett = commands.getoutput('date "+%Y-%m-%d %H:%M:%S"')
                            time2 = transfertime(timett)
                        except Exception,e:
                            print e
                            log('时间格式错误')
                            self.request.send('时间格式错误')
                        if int(time1) > int(time2):
			    print ret
                            os.popen('date -s "%s"' % ret).read()
                            self.request.send('时间修改成功')
                        else:
			    print ret
                            self.request.send('已经收到请求，成功处理...')
                            stopjava()
                            time.sleep(20)
                            os.popen('date -s "%s"' % ret).read()
                            startjava()
                            time.sleep(10)
                else:
                    log('the source is wrong')
                    pass
            except KeyboardInterrupt:
                log('键盘错误')
#server = Server((HOST,PORT),Handler)
def funzioneDemo():
    server = ThreadingServer((HOST,PORT),Handler)
    server.serve_forever()
def createDaemon():
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError,error:
        print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print 'Daemon PID %d' % pid
            os._exit(0)
    except OSError,error:
        print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
        os._exit(1)
        funzioneDemo()
if __name__ == "__main__":
    createDaemon()









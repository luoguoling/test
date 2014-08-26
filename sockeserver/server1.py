#coding:utf-8
import socket
import sys
host = "127.0.0.1"
port = 30000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)
while 1:
    clientsock,clientaddr = s.accept()
    while 1:
        buf = clientsock.recv(200)
        if len(buf) != 0:
            print buf
            if buf[len(buf)-1] == "\n":
                break
#                continue
    clientsock.close()

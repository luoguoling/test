#coding:utf-8
import socket
host = "127.0.0.1"
port = 30000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.send("jojojjjjjjjjjjjjjjjjjw34234" + "\r\n")
s.close()

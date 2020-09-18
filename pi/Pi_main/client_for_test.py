import socket
import sys
import os
s = socket.socket()
num=7
s.connect(("ssafyteam7.iptime.org",9999))
s.send(bytes(str(num),'utf8'))
s.close()

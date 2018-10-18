# coding=utf8
# author:kang
# 获取本机IP地址

import socket
import os,sys

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

class get_ip():
    def __init__(self):
        pass
    def do(self):
        #获取本机机器名
        myname = socket.getfqdn(socket.gethostname(  ))
        #获取本机IP地址
        myaddr = socket.gethostbyname(myname)
        return myaddr
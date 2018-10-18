# coding=utf8
# author:kang
# 自动化测试客户端执行文件

import unittest,time,sys,os,shutil,logging
from datetime import datetime
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

import Client.lib.get_ip as get_ip

host_name=get_ip.get_ip().do()
exe_cmd="start cmd /c @echo start client..... & start /wait cmd /c python ../lib/connect_server.py "+host_name+" "+"up"+"& start /wait cmd /c python Runner.py & start /wait cmd /c python ../lib/connect_server.py "+host_name+" "+"down"
os.system(exe_cmd)

        



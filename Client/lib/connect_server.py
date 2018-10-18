# coding=utf8
# author:kang
# APP UI 自动化测试执行

import sys,os
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

import Client.lib.load_data as load_data

host_name = sys.argv[1]
status = sys.argv[2]
slave_class = load_data.set_slave(host_name,status)
slave = slave_class()
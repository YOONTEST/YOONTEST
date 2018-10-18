# coding=utf8
# author:kang
# 自动化测试脚本启动文件

import unittest,time,sys,os,shutil,logging
from datetime import datetime
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

import Client.lib.load_data as load_data
import Client.setting.variable as variable
import Client.lib.get_ip as get_ip

host_name=get_ip.get_ip().do()
print("Slave "+host_name+" is started...")
while True:
    get_activity_class=load_data.get_activity(host_name)
    activity = get_activity_class()
    activity_id = activity.get("activity_id")
    if activity_id:
        exe_cmd="python "+variable.get_variable().HOME+"\Client\main.py"
        os.system(exe_cmd)
    else:
        time.sleep(30)
        


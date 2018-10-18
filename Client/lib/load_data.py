# coding=utf8
# author:kang
# 从数据库加载测试数据

import os,sys,logging
import datetime
import requests
import urllib

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class test_cases(object):
    def __init__(self,slave):
        self.slave=slave
    
    def __call__(self):
        activity_class = get_activity(self.slave)
        activity=activity_class()
        plan_name = activity.get("plan_name")
        activity_id = activity.get("activity_id")
        test_type = activity.get("test_type")
        device_name = activity.get("device")
        run_list_class = run_list(plan_name)
        run_lists = run_list_class()
        
        data = {"run_list":run_lists,"activity_id":activity_id,"test_type":test_type,"device_name":device_name}
        return data

class run_list():
    def __init__(self,plan_name):
        self.plan_name = plan_name
    
    def __call__(self):
        url="http://10.10.11.16/run-list/?plan_name="+self.plan_name
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result["data"]
    
class test_case():
    def __init__(self,scenario_name,testcase_name,test_type):
        self.scenario_name = scenario_name
        self.testcase_name = testcase_name
        self.test_type = test_type
    def __call__(self):
        url="http://10.10.11.16/test-case/?testcase_name="+self.testcase_name+"&scenario_name="+self.scenario_name+"&test_type="+self.test_type.lower()
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result["data"] 
    
class get_activity():
    def __init__(self,slave):
        self.slave=slave
    def __call__(self):
        url="http://10.10.11.16/get-activity/?slave="+self.slave
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result.get("data")
    
class get_device():
    def __init__(self,device):
        self.device=device
    def __call__(self):
        url="http://10.10.11.16/get-device/?device="+self.device
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result.get("data")
    
class set_activity():
    def __init__(self,activity_id,status):
        self.activity_id = activity_id
        self.status = status
    def __call__(self):
        url="http://10.10.11.16/set-activity/?activity_id="+str(self.activity_id)+"&status="+self.status
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result.get("data")

class set_slave():
    def __init__(self,slave,status):
        self.slave = slave
        self.status = status
    def __call__(self):
        url="http://10.10.11.16/slave/?slave="+self.slave+"&status="+self.status
        self.request=requests.get(url)
        self.result = self.request.json()
        return self.result.get("data")
    
class upload_result():
    def __init__(self,data):
        self.data = data
        
    def do(self):
        url="http://10.10.11.16/upload-result/?data="+urllib.request.quote(str(self.data))
        results = requests.get(url)

#print(load_data_web().get_test_details("WEB自动化测试"))
#print(load_data_api().get_test_details("自动化测试"))
#print(get_activity().get("10.10.12.23"))
# coding=utf8
# author:kang
##############主类####################
#0.使用 unittest 框架为基础 
#1.通过接口获取测试类型，测试用例列表
#2.通过脚本生成测试用例脚本
#3.通过接口上传每个测试用例的结果
#4.屏幕输出测试结果概要
#5.通过接口发送测试结果概要到企业微信
####################################

import unittest
import time
import sys
import os
import logging
from datetime import datetime
#import requests
#import urllib
#import shutil
#import threading
#import random

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

import Client.driver.api_driver as api_driver
import Client.driver.app_driver as app_driver
import Client.driver.web_driver as web_driver

import Client.lib.load_data as load_data
import Client.lib.initial as initial
import Client.setting.variable as variable
import Client.lib.wework_notify as wework_notify
import Client.lib.get_ip as get_ip

#生成log
initial.init().launch()
logfile=time.strftime('%Y-%m-%d',time.localtime(time.time())) 
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename=variable.get_variable().LOGFOLDER+logfile+'.log',filemode='w')

#===========================获取测试数据============================
host_name=get_ip.get_ip().do()  #获取本机IP
run_data=load_data.test_cases(host_name) #获取执行用例列表+活动ID
data = run_data()
run_list = data.get("run_list")
total = len(run_list)
activity_id = data.get("activity_id")
test_type = data.get("test_type")
device_name = data.get("device_name")
logging.info(device_name)
set_activity_calss = load_data.set_activity(activity_id, "running")
set_activity_calss()
device_class = load_data.get_device(device_name)
device = device_class()
device = device.get("device_info")
if device:
    device = ""

scenario_list=[]
for i in run_list:
    scenario_list.append(i.get("scenario_name"))
scenario_list = list(set(scenario_list))
scenario_list.sort()

if test_type == "API":   #判断是否是接口测试？
    test_type_str = '''running =api_driver.driver(self)  
        self.testcase_result = running()''' #调用接口测试驱动
elif test_type == "WEB": #判断是否是WEB测试？
    test_type_str = '''running=web_driver.driver(self)
        self.testcase_result = running()''' #调用WEB测试驱动
elif test_type == "APP": #判断是否是APP测试？
    test_type_str = '''running=app_driver.driver(self)
        self.testcase_result = running()''' #调用APP测试驱动
else:
    pass
test_data_details={"total":total,"success":0,"failures":0,"errors":0,"details":{}}
#=======================生成测试用例脚本=============================
scenarios_class=""
scenarios_str={}
#生成测试用例
for scenario_name in scenario_list:
    case_str=""
    for case in run_list:
        if scenario_name==case.get("scenario_name"):
            testcase_name = case.get("testcase_name")
            case_str=case_str+u'''
    def '''+testcase_name+u'''(self):
        self.testcase_name=sys._getframe().f_code.co_name
        self.test_type = "'''+test_type+u'''"
        self.device = "'''+device+u'''"
        logging.info('####################测试集 {sn} : 测试用例 {tn} 开始####################'.format(tn=self.testcase_name,sn=self.scenario_name))
        self.testcase_result={}
        self.global_parameters={}
        self.upload_results={}
        '''+test_type_str+u'''
        self.global_parameters=self.testcase_result.get("global_parameters")
        self.upload_results = self.testcase_result
        self.upload_results["test_type"] = test_type
        self.upload_results["scenario_name"] = self.scenario_name
        self.upload_results["activity_id"] = activity_id
        
        if self.upload_results.get("class"):
            del self.upload_results["class"]
        if self.upload_results.get("check_type"):
            del self.upload_results["check_type"]
        if self.upload_results.get("session"):
            del self.upload_results["session"]
        if self.upload_results.get("cookies"):
            del self.upload_results["cookies"]
        load_data.upload_result(self.upload_results).do()
        
        logging.info('####################测试集 {sn} : 测试用例 {tn} 结束####################'.format(tn=self.testcase_name,sn=self.scenario_name))
'''          
    scenarios_str[scenario_name]=case_str
    
for scenario_name in scenario_list:   
    scenarios_class = scenarios_class +u'''
class '''+scenario_name+u'''(unittest.TestCase):
    def setUp(self):
        self.scenario_name=self.__class__.__name__
        
    '''+scenarios_str[scenario_name]+u'''
    
    def tearDown(self):
        try:
            if self.testcase_result.get("tc_result")=="error":
                test_data_details["errors"]=test_data_details["errors"]+1 
                
            elif self.testcase_result.get("tc_result")=="fail":
                test_data_details["failures"]=test_data_details["failures"]+1
                self.testcase_result["tc_result_msg"]=self.testcase_result["tc_result_msg"].split(" : ")[1]
                self.assertTrue(False,self.testcase_result["tc_result_msg"])
            else:
                self.testcase_result["tc_result"]="pass"
                test_data_details["success"]=test_data_details["success"]+1 
        except AssertionError:
            pass
            
        key_str=self.scenario_name+"-"+self.testcase_name
        test_data_details["details"][key_str]=self.testcase_result
'''
#print(scenarios_class)
exec(scenarios_class) 

#添加测试用例到用例集
suite = unittest.TestSuite()
for case in run_list:
    scenario_name = case.get("scenario_name")
    testcase_name=  case.get("testcase_name")
    exec("suite.addTest("+scenario_name+"('"+testcase_name+"'))")         
exec("suite=unittest.TestSuite([suite])")


if __name__ == '__main__':   
    print("Running...") #开始提示打印
    start_time=datetime.now()  #本质脚本执行开始时间
    runner=unittest.TextTestRunner()   #使用TestTestRunner执行
    result = runner.run(suite) #执行测试用例集
    end_time=datetime.now()   #本支持脚本执行结束时间
    duration=end_time-start_time   #总执行时间
    success=test_data_details["success"]
    failures=test_data_details["failures"]
    errors=test_data_details["errors"]
    time.sleep(1)
    summary_data={"start_time":str(start_time),"end_time":str(end_time),"duration":str(duration),"total":str(total),"success":str(success),"failures":str(failures),"errors":str(errors)}
    print("+++++++++++++++++++++测试结果汇总++++++++++++++++++++++++")
    print("开始时间: "+str(start_time))
    print("结束时间: "+str(end_time))
    print("消耗时间: "+str(duration))
    print("总用例数: "+str(total))
    print("成功: "+str(success))
    print("失败: "+str(failures))
    print("错误: "+str(errors))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(test_data_details)
    if int(total):
        wework_notify.wework_notify().sent(summary_data,variable.get_variable().ww_member_to, variable.get_variable().ww_team_to)#企业微信消息推送
        
    set_activity_calss = load_data.set_activity(activity_id, "finished")
    set_activity =  set_activity_calss()

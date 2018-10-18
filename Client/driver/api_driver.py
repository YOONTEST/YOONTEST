# coding=utf8
# author:kang
###############接口测试驱动#################################

import os,sys,logging,time
from datetime import datetime
import requests
import unittest

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

from Client.lib.load_data import test_case

#######################API DRIVER#############################   
class driver():
    def __init__(self,scenariosclass):
        self.scenariosclass = scenariosclass
        self.testcase_name = scenariosclass.testcase_name
        self.testscenarios_name = scenariosclass.scenario_name
        self.test_type = scenariosclass.test_type
        test_data = test_case(self.testscenarios_name,self.testcase_name,self.test_type)
        self.test_cases = test_data()
        
    def __call__(self):
        self.test_case_data = {}
        self.test_case_data["testcase_name"] = self.testcase_name
        self.test_case_data["class"] = self.scenariosclass
        self.test_case_data["which"] =self.test_cases[0]["which"]                 #接口URL
        self.test_case_data["how"] =self.test_cases[0]["how"]                     #接口方法
        self.test_case_data["headers"]=self.test_cases[0]["headers"]              #接口返回headers
        self.test_case_data["body"]=self.test_cases[0]["body"]                    #接口返回body
        self.test_case_data["expected"]=self.test_cases[0]["expected"]            #接口返回期望结果
        self.test_case_data["check_type"] = self.test_cases[0]["check_type"]      #断言类型
        self.test_case_data["cookies"]=""
        self.test_case_data["session"]=requests.Session()
        
        start_time=datetime.now()                                                 #测试用例开始时间
        self.this_step = eval("rest(self.test_case_data)."+self.test_case_data["how"])                 #执行接口请求
        self.test_case_data = self.this_step()
        end_time=datetime.now()                                                   #用例结束时间
        
        duration=end_time-start_time    #用例执行时间
        self.test_case_data["duration"]=str(duration)                             #执行时间转换为字符串
        self.test_case_data["start_time"]=str(start_time)                         #测试开始时间转换成字符串
        self.test_case_data["end_time"]=str(end_time)                             #测试结束时间转换成字符串
        return self.test_case_data
    
##############GET#################################
class rest():
        #点击页面对象
    def __init__(self,test_case_data):
        self.test_case_data = test_case_data
        self.testcase_name = self.test_case_data["testcase_name"]
        self.how =self.test_case_data["how"]
        self.which=self.test_case_data["which"]
        self.headers=self.test_case_data["headers"]
        self.body=self.test_case_data["body"]
        self.expected =self.test_case_data["expected"]
        self.check_type=self.test_case_data["check_type"]
        self.scenariosclass = self.test_case_data["class"]
        self.session=self.test_case_data["session"]
        self.cookies=self.test_case_data["cookies"]
        
    def get(self): #请求GET
        try:
            self.request=self.session.get(self.which,headers=self.headers,verify=False)
            self.test_case_data["response_time"]=str(int(self.request.elapsed.total_seconds()*1000))
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            self.request=""
            self.test_case_data["response_results"]=e
            self.test_case_data["response_time"]="0"
    
        return self.do(self.request)
     
    def post(self): #请求POST
        try:
            self.request=self.session.post(self.which,headers=self.headers,json=self.body,verify=False)
            self.test_case_data["response_time"]=str(int(self.request.elapsed.total_seconds()*1000))
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            self.request=""
            self.test_case_data["response_results"]=e
            self.test_case_data["response_time"]="0"
            
        return self.do(self.request)
        
    def put(self): #请求PUT
        try:
            self.request=self.session.put(self.which,headers=self.headers,json=self.body,verify=False)
            self.test_case_data["response_time"]=str(int(self.request.elapsed.total_seconds()*1000))
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            self.request=""
            self.test_case_data["response_results"]=e
            self.test_case_data["response_time"]="0"
            
        return self.do(self.request)
    
    def delete(self): #请求delete
        try:
            self.request=self.session.delete(self.which,headers=self.headers,json=self.body,verify=False)
            self.test_case_data["response_time"]=str(int(self.request.elapsed.total_seconds()*1000))
            #logging.info(self.request)
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            self.request=""
            self.test_case_data["response_results"]=e
            self.test_case_data["response_time"]="0"
            
        return self.do(self.request)    
    

    def do(self,request): #处理返回信息
        self.request=request
        if self.request:
            self.result = str(self.request.json())
            self.result = self.result.replace(u'\u2022',u'·').replace(u'\xa0', u' ').replace(u'\xb2', u' ').replace(u'\u2070', u' ').replace(u'\xb9', u' ').replace(u'\u2078', u' ')

            self.result = eval(self.result)
            self.test_case_data["response_results"]=self.result
            #logging.info(self.result)

            self.testcase_result=check_dict().check(self.result, self.expected,self.check_type,self.scenariosclass)
            self.test_case_data["tc_result"]=self.testcase_result["result"]
            self.test_case_data["tc_result_msg"]=self.testcase_result["msg"]

        else:
            self.test_case_data["tc_result"]="error"
            self.test_case_data["tc_result_msg"]="请求失败"
            logging.info("请求失败")  
        return self.test_case_data
    

#############CHECK##############################
class check_text(unittest.TestCase):
    #比较页面对象的文本与期望的文本
    def check(self,actual,expected,action,stepclass):
        self._actual=actual
        self._expected=eval(expected)
        self._action=action
        self.stepclass=stepclass
        self.testcase_name=stepclass.testcase_name
        
        self.this_check=eval("self."+self._action)
        self.data={}
        self.testcase_result=self.this_check()
        return self.testcase_result
        
    def equal(self):
        #文本精确检查
        try:     
            #self.stepclass.assertEqual(str(self._actual),str(self._expected),"实际结果中没有找到期望的测试数据   '"+str(self._expected)+"'")
            if str(self._actual)==str(self._expected):
                logging.info("实际结果中找到期望的测试数据  '"+str(self._expected)+"' - Pass")
                self.testcase_result={"result":"pass","msg":""}
            else:
                logging.info("实际结果中没有找到期望的测试数据   '"+str(self._expected)+"' - Fail")
                self.stepclass.assertTrue(False,"实际结果中没有找到期望的测试数据   '"+str(self._expected)+"'")

            return self.testcase_result
        
        except AssertionError as e:
            self.testcase_result={"result":"fail","msg":str(e)}
            return self.testcase_result
        
class check_dict(unittest.TestCase):
    #比较页面对象的文本与期望的文本
    def check(self,actual,expected,action,stepclass):
        self._actual=actual
        self.expected=eval(expected)
        self._action=action
        self.stepclass=stepclass
        self.testcase_name=stepclass.testcase_name
        
        self.this_check=eval("self."+self._action)
        self.data={}
        self.testcase_result=self.this_check()
        return self.testcase_result
        
    def equal(self):
        #文本精确检查
        if self.expected:
            for i in range(len(self.expected)):
                self.expect=self.expected[i]
                try:
                    for key in self.expect:
                        expect=str(self.expect[key])
                        actual= str(self.get_value_from_dict(self._actual,key,expect))
                    
                        if expect==actual:
                            logging.info("实际结果中找到期望的测试数据   '"+expect+"' - Pass")
                            self.testcase_result={"result":"pass","msg":""}
                        else:
                            logging.info("实际结果中没有找到期望的测试数据   '"+expect+"' - Fail")
                            self.stepclass.assertTrue(False,"实际结果中没有找到期望的测试数据 '"+expect+"'")
                            self.testcase_result={"result":"Fail","msg":"实际结果中没有找到期望的测试数据 "}
                except AssertionError as e:
                    self.testcase_result={"result":"fail","msg":str(e)}
                    break
        else:
            self.testcase_result={"result":"pass","msg":""}
        return self.testcase_result
            

    def get_value(self,x,keys):
        for key in x:
            if key==keys:
                return x.get(key)

    def is_dic_or_list(self,x):
        if isinstance(x,dict):
            return "dict"
        elif isinstance(x,list):
            return "list"
        else:
            return "unknown"

    def get_value_from_dict(self,x,keys,values):
        data=[]
        if self.is_dic_or_list(x)=="dict" and keys in x:
            data.append(str(self.get_value(x,keys)))
        elif self.is_dic_or_list(x)=="dict":
            for key in x:
                xx = x.get(key)
                if self.is_dic_or_list(xx)=="dict" and keys in xx:
                    data.append(self.get_value(xx,keys))
                elif self.is_dic_or_list(xx)=="dict":
                    for key in xx:
                        xxx=xx.get(key)
                        if self.is_dic_or_list(xxx)=="dict" and keys in xxx:
                            data.append(self.get_value(xxx,keys))
                        elif self.is_dic_or_list(xxx)=="dict":
                            for key in xxx:
                                xxxx=xxx.get(key)
                                if self.is_dic_or_list(xxxx)=="dict" and keys in xxxx:
                                    data.append(self.get_value(xxxx,keys))
                                elif self.is_dic_or_list(xxxx)=="dict":
                                    for key in xxxx:
                                        xxxxx=xxxx.get(key)
                                        if self.is_dic_or_list(xxxxx)=="dict" and keys in xxx:
                                            data.append(self.get_value(xxx,keys))
                                        elif self.is_dic_or_list(xxxxx)=="dict":
                                            pass
                                        elif self.is_dic_or_list(xxxxx)=="list":
                                            for i in range(len(xxxxx)):
                                                if xxxxx:
                                                    xxxxxx=xxxxx[i]
                                                    if self.is_dic_or_list(xxxxxx)=="dict" and keys in xxxxxx:
                                                        data.append(self.get_value(xxxxxx,keys))
                                                    elif self.is_dic_or_list(xxxxxx)=="dict":
                                                        pass

                        elif self.is_dic_or_list(xxx)=="list":
                            for i in range(len(xxx)):
                                if xxx:
                                    xxxx=xxx[i]
                                    if self.is_dic_or_list(xxxx)=="dict" and keys in xxxx:
                                        data.append(self.get_value(xxxx,keys))
                                    elif self.is_dic_or_list(xxxx)=="dict":
                                        for key in xxxx:
                                            xxxxx=xxxx.get(key)
                                            if self.is_dic_or_list(xxxxx)=="dict" and keys in xxx:
                                                data.append(self.get_value(xxx,keys))
                                            elif self.is_dic_or_list(xxxxx)=="dict":
                                                pass
                                            elif self.is_dic_or_list(xxxxx)=="list":
                                                for i in range(len(xxxxx)):
                                                    if xxxxx:
                                                        xxxxxx=xxxxx[i]
                                                        if self.is_dic_or_list(xxxxxx)=="dict" and keys in xxxxxx:
                                                            data.append(self.get_value(xxxxxx,keys))
                                                        elif self.is_dic_or_list(xxxxxx)=="dict":
                                                            pass

                elif self.is_dic_or_list(xx)=="list":
                    for i in range(len(xx)):
                        if xx:
                            xxx=xx[i]
                            if self.is_dic_or_list(xxx)=="dict" and keys in xxx:
                                data.append(self.get_value(xxx,keys))
                            elif self.is_dic_or_list(xxx)=="dict":
                                pass

        elif self.is_dic_or_list(x)=="list":
            for i in range(len(x)):
                if xx:
                    xx=x[i]
                    if self.is_dic_or_list(xx)=="dict" and keys in xx:
                        data.append(self.get_value(xx,keys))
                    elif self.is_dic_or_list(xx)=="dict":
                        for key in xx:
                            xxx=xx[key]
                            if self.is_dic_or_list(xx)=="dict" and keys in xx:
                                data.append(self.get_value(xx,keys))
                            elif self.is_dic_or_list(xx)=="dict":
                                pass
                            elif self.is_dic_or_list(xx)=="list":
                                pass             

        #logging.info(data)
        if values in data:
            return values
        else:
            return None

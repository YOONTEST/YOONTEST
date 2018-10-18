# coding=utf8
# author:kang
# 企业微信消息推送

import os,sys,time
import logging
import requests

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)
  
class wework_notify():  
    def sent(self,contents,member,team): 
        #contents - 消息内容 json格式
        #member - 企业微信账号 ['xxx']
        #team - 企业微信组   
        if int(contents.get('errors'))>0:
            con_str='''测试结果中有错误的测试用例！！！'''
        elif int(contents.get('failures'))>0:
            con_str='''测试结果中有失败的测试用例！！！'''
        else:
            con_str='''全部测试用例执行成功！！！'''
        con_str=con_str+'''
结果如下： 
开始时间: '''+contents.get('start_time')+'''
结束时间: '''+contents.get('end_time')+'''
消耗时间: '''+contents.get('duration')+'''
总用例数: '''+contents.get('total')+'''
成功: '''+contents.get('success')+'''
失败: '''+contents.get('failures')+'''
错误: '''+contents.get('errors')   

        self._which="https://captain.qianbaocard.org/api/ops/wx/message/txt"
        self.what={"corpId":"ww95eb4f3c74ea7128","agentId": "1000050","payload": con_str,"users": member,"parties": team,"tags": [""]}

        autho_request= requests.post(self._which,json=self.what)
        result = autho_request.json()
        if str(autho_request.status_code)=="200":
            logging.info("sent success")
            #print("sent success")
        else:
            logging.info("sent fail")
            #print("sent fail")

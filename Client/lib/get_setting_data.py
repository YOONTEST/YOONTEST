# coding=utf8
# author:kang
# 全局变量设置
import os,sys,requests
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

class get_setting_from_db():
    def __init__(self):
        pass
    def get_value(self,key_name):
        self.url="http://10.10.11.16/get-setting/?key_name="+key_name
        self.request=requests.get(self.url)
        self.result = self.request.json()["data"]
        for i in self.result:
            if i["key_name"]==key_name:
                return i["key_value"]
            else:
                return ""
            
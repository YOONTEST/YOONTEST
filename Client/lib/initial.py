# coding=utf8
# author:kang
# 初始化目录

import sys,os

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

from Client.setting import variable

#-------------Initialization work folders-------------------------------
class init():
    def __init__(self):
        pass
        
    def launch(self):
    #创建测试结果目录
        #WEB
        if not os.path.exists(variable.get_variable.REPORTFOLDER):
            os.makedirs(variable.get_variable.REPORTFOLDER)
        if not os.path.exists(variable.get_variable.LOGFOLDER):
            os.makedirs(variable.get_variable.LOGFOLDER)
        if not os.path.exists(variable.get_variable.SCREENFOLDER):
            os.makedirs(variable.get_variable.SCREENFOLDER)


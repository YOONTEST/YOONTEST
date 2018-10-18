# coding=utf8
# author:kang
# 全局变量设置
import os,sys,requests
from Client.lib.get_setting_data import get_setting_from_db
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)
        
class get_variable():
    
    def __init__(self):
        pass
    
    APP_DRIVER=""
    
    
    #测试类型
    API_TEST="api"
    APP_TEST="app"

    #获取当前目录
    #HOME=os.getcwd()
    HOME=os.path.abspath('..')
    
    #测试报告目录
    #----------WEB    
    LOGFOLDER=HOME+"/Result/logs/"
    SCREENFOLDER=HOME+"/Result/screenshot/"
    REPORTFOLDER=HOME+"/Result/report/"

    #驱动目录
    CHROME_DRIVER="../Client/driver/webdriver/chromedriver.exe"  

#-----------本地测试数据库配置-------------------    
    host = "10.10.11.16"
    port = "3306"
    db   = "auto"
    user = "qianbao"
    password = "qb123"
    
    #API全局变量-------------------------------
    COOKIES={}
    SESSION=""
    TOKEN=""
    
    #企业微信消息推送----------------------------------
    ww_member_to=['sh1659']
    ww_team_to=['']
    #ww_team_to=['672']
    
    #Mongo db-----------------------------------------
    #MONGO_DB=get_setting_from_db().get_value("MONGO_DB")
    
    #------邮箱设置---------------
    #TO=get_setting_from_db().get_value("TO")
    #FAIL_TO=get_setting_from_db().get_value("FAIL_TO")
    #ERROR_TO=get_setting_from_db().get_value("ERROR_TO")
    #FROM=get_setting_from_db().get_value("ERROR_TO")
    #SMTP_SERVER=get_setting_from_db().get_value("SMTP_SERVER")
    #EMAIL_USER=get_setting_from_db().get_value("EMAIL_USER")
    #EMAIL_PWD=get_setting_from_db().get_value("EMAIL_PWD")
    #FROM="monitor@qianbaocard.com"
    #SMTP_SERVER="hwimap.exmail.qq.com" 
    #EMAIL_USER="monitor@qianbaocard.com"
    #EMAIL_PWD="Qbsh0919"
    
get_variable()
 
 
 

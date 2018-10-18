# coding=utf8
# author:kang
# 发送邮件
import os,sys,time,smtplib,logging
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication 
import Client.setting.variable as variable
from datetime import  datetime
import time
curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

#-----------send email-------------------------
class email():
    def __init__(self):
        pass
         
    def send(self,subject,attach_path,attach_name,name,all,summary):
        #print(name)
        #print(all)
        #print(summary)
        a=int(summary['error'])
        b=len(all)
        c=int(summary['pass'])
        f=str(summary['fail'])
        erroras=a/b*100
        passas=c/b*100
        errornum=str(erroras)
        passnum=str(passas)
        errora=str(erroras)
        passa=str(passas)
        stara=all[0]["starttime"]
        end=all[0]["endtime"]
        star=str(stara)
        stara=datetime.strptime(star,"%Y-%m-%d %H:%M:%S.%f")
        enda=datetime.strptime(end,"%Y-%m-%d %H:%M:%S.%f")
        full_runtimea=enda-stara
        full_runtime=str(full_runtimea)
        times=time.strftime("%Y-%m-%d %H:%M:%S")
        timea=str(times)    
        cases=len(all)
        case=str(cases)    
        error=str(a)
        peass=str(c)
        #print(peass)
        #打印类型排查问题
        
        if int(summary["fail"])>0:
            self.to=variable.get_variable().FAIL_TO
            mail_body=('<html><body><p>各位好：</p><p>&nbsp;&nbsp;【'+name+'】'+timea+'接口自动化测试结果如下：</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 1.总用例数：'+case+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 2.执行成功数：'+peass+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 3.执行错误数：：'+error+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 4.执行错误率：'+errornum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 5.执行成功率：'+passnum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 6.开始时间：'+star+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 7.结束时间：'+end+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 8.共执行时间：'+full_runtime+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 如有疑问请联系测试组：</p><p>&nbsp;&nbsp;&nbsp;&nbsp&ltshtest@qianbaocard.com&gt</p><p>&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; 谢谢！</p></body></html>')
            subject=subject+" - Warning!!!"
            
        elif int(summary['error'])>0:
            self.to=variable.get_variable().ERROR_TO
            mail_body=('<html><body><p>各位好：</p><p>&nbsp;&nbsp;【'+name+'】'+timea+'接口自动化测试结果如下：</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 1.总用例数：'+case+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 2.执行成功数：'+peass+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 3.执行错误数：：'+error+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 4.执行错误率：'+errornum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 5.执行成功率：'+passnum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 6.开始时间：'+star+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 7.结束时间：'+end+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 8.共执行时间：'+full_runtime+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 如有疑问请联系测试组：</p><p>&nbsp;&nbsp;&nbsp;&nbsp&ltshtest@qianbaocard.com&gt</p><p>&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; 谢谢！</p></body></html>')
            subject=subject+" - ERROR!!!"
            
        else:
            self.to=variable.get_variable().TO
            mail_body=('<html><body><p>各位好：</p><p>&nbsp;&nbsp;【'+name+'】'+timea+'接口自动化测试结果如下：</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 1.总用例数：'+case+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 2.执行成功数：'+peass+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 3.执行错误数：：'+error+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 4.执行错误率：'+errornum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 5.执行成功率：'+passnum+'%</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 6.开始时间：'+star+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 7.结束时间：'+end+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 8.共执行时间：'+full_runtime+'</p><p>&nbsp;&nbsp;&nbsp;&nbsp; 如有疑问请联系测试组：</p><p>&nbsp;&nbsp;&nbsp;&nbsp&ltshtest@qianbaocard.com&gt</p><p>&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; 谢谢！</p></body></html>')
        if "," in self.to:
            self.to=self.to.split(",")
            
        msg = MIMEMultipart() 
        msg["Subject"] = subject
        msg["From"]  = variable.get_variable().FROM
        msg["To"]   = variable.get_variable().TO

        #---这是文字部分--- 
        part = MIMEText(mail_body,'html','utf-8') 
        msg.attach(part) 
   
        #---这是附件部分--- 
        part = MIMEApplication(open(attach_path+attach_name,'rb').read()) 
        part.add_header('Content-Disposition', 'attachment', filename=attach_name) 
        msg.attach(part) 
   
        s = smtplib.SMTP(variable.get_variable().SMTP_SERVER, timeout=60)
        s.login(variable.get_variable().EMAIL_USER,variable.get_variable().EMAIL_PWD)
        s.sendmail(variable.get_variable().FROM,self.to, msg.as_string())
        s.close()
        logging.info("email sent")

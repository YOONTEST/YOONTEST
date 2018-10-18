# coding=utf8
# author:kang

##############WEB测试驱动#########################################
#1.使用 uiautomator2 作为底层驱动
#2.获取测试用例的测试数据，如：操作，被操作的页面对象，输入输入的内容，断言类型，期望结果。。。
#3.需要初始化                             :  python -m uiautomator2 init
#4.安装并运行 weditor :  python -m weditor
###############################################################

import os,sys,time
from datetime import datetime
import logging
import unittest
import uiautomator2

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

from Client.lib.load_data import test_case
from Client.setting.variable import get_variable

################## 启动CHROME ###############################
class app(unittest.TestCase): 
    def launch(self,data): #连接设备
        #data={"ip":"10.10.20.26","package":"com.tencent.mm","activity":"com.tencent.mm"}
        logging.info(data)
        self.ip = data.get("ip")
        self.device=""
        try:
            self.device = uiautomator2.connect(self.ip)  #连接设备
            self.device.screen_on()                      #打开屏幕
            #self.device.unlock()
        except Exception as e:
            logging.error(e)
        return self.device
        
    def open(self,data):
        self.driver = data.get("driver")
        self.package = data.get("device").get("package")
        self.activity = data.get("device").get("activity")
        
        logging.info(self.driver)
        logging.info(self.package)
        logging.info(self.activity)
        
        if self.driver:
            logging.info("device connected!!!")
        else:
            return {"result":"error","message":"driver connection failed!!!"}
        try:
            self.close(data) #关闭APP
            time.sleep(2)
            self.driver.app_start(self.activity) #启动APP
            time.sleep(10)
            logging.info("app launched!!!")
            self.step_result={"result":"pass","msg":""}
        except Exception as e:
            logging.error(e)
            self.step_result={"result":"fail","msg":"launch app failed"}
        return self.step_result

    def close(self,data):
        self.driver = data.get("driver")
        self.package = data.get("device").get("package")
        try:
            self.driver.app_stop(self.package) #关闭APP
            time.sleep(1)
            self.device.screen_off()                      #关闭屏幕
            logging.info("driver is closed!!!")
            self.testcase_result={"result":"pass","msg":""}
        except Exception as e:
            logging.error(e)
            self.testcase_result={"result":"fail","msg":"close driver failed"}
        return self.testcase_result
    
######################################################
class driver():
    def __init__(self,scenariosclass):
        self.scenariosclass = scenariosclass
        self.testcase_name = scenariosclass.testcase_name
        self.testscenarios_name = scenariosclass.scenario_name
        self.test_type = scenariosclass.test_type
        self.device = scenariosclass.device
        test_data = test_case(self.testscenarios_name,self.testcase_name,self.test_type)
        self.test_cases = test_data()
        
    def __call__(self):
        self.test_case_data = {}
        self.test_case_data["testcase_name"] = self.testcase_name
        self.test_case_data["class"] = self.scenariosclass
        self.test_case_data["step"] = []
        self.test_case_data["device"] = self.device
        self.test_case_data["driver"] = app().launch(self.test_case_data["device"]) #启动浏览器
        start_time=datetime.now()
        
        for one_step in self.test_cases:
            self.step_data={}
            self.step_data["driver"] = self.test_case_data["driver"]
            self.step_data["device"] = self.test_case_data["device"]
            self.step_data["testcase_name"] = self.test_case_data["testcase_name"]
            self.step_data["class"] = self.test_case_data["class"]
            self.step_data["step_name"] =one_step.get("step_name")
            self.step_data["how"] = one_step.get("how")
            self.step_data["which"] = one_step.get("which")
            self.step_data["what"] = one_step.get("what")
            self.step_data["expected"] = one_step.get("expected") 
            self.step_data["check_type"] = one_step.get("check_type")                                     
            self.this_step = eval("action(self.step_data)."+self.step_data["how"])                  #执行接口请求
            logging.info("####################"+self.step_data["step_name"]+"####################")
            test_step_data = self.this_step()
            self.test_case_data["step"].append(test_step_data)
        
        
        end_time=datetime.now()                                                                     #用例结束时间
        duration=end_time-start_time    #用例执行时间
        self.test_case_data["duration"]=str(duration)                                               #执行时间转换为字符串
        self.test_case_data["start_time"]=str(start_time)                                           #测试开始时间转换成字符串
        self.test_case_data["end_time"]=str(end_time)                                               #测试结束时间转换成字符串
        
        return self.test_case_data

##################页面操作####################################
class action():
    def __init__(self,step_data):
        self.step_data = step_data
        self.testcase_name = self.step_data["testcase_name"]
        self.scenariosclass = self.step_data["class"]
        self.driver = self.step_data["driver"]
        self.step_name = self.step_data["step_name"]

    def open(self):
        logging.info(self.step_data)
        self.step_result = app().open(self.step_data)
        #screen(self.step_data,3).do()
        return self.step_result
    
    def close(self):
        self.step_result= app().close(self.step_data)
        #screen(self.step_data,3).do()
        return self.step_result
    
    def click(self):
        click_class = click(self.step_data)
        self.step_result = click_class()
        screen(self.step_data,3).do
        return self.step_result
        
    
    def input(self):
        input_class = input_text(self.step_data)
        self.step_result = input_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def swipe(self):
        swipe_class = swipe(self.step_data)
        self.step_result = swipe_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def wait(self):
        time.sleep(int(self.test_step_data["what"]))
        logging.info("script waiting for "+str(int(self.test_step_data["what"])))
        self.step_result={"result":"pass","msg":"script waiting for "+str(int(self.test_step_data["what"]))}
        return self.step_result
        
    def get_text(self):
        get_text_class = get_text(self.step_data)
        self.step_result = get_text_class()
        return self.step_result
    
    def code(self):
        code_class = code(self.step_data)
        self.step_result = code_class()
        screen(self.step_data,3).do()
        return self.step_result

####################################################################
class find(): #查找页面对象
    def __init__(self,step_data):
        self.data={}
            
    def __call__(self):
    #查找一个页面对象          
        for i in range(5):
            driver=self.step_data.get("driver")
            self.which=self.step_data.get("which")
            self.what=self.step_data.get("what")
            self.testcaseclass=self.step_data.get("class")
            try:
                self.element = eval(self.which)  #根据uiautomator 查询对象
                if self.element.info.get("enabled"):
                    logging.info("found")
                    break
            except Exception as e:
                print(e)
            time.sleep(1)
                                   
        if self.element=="":
            logging.warning(self.which+" does not found")
            return False

class get_text(): #根据 xpath 查找对象，并获取文本 
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.step_data)
        self.element=find_class()
        
        if (self.element!=False):
            data=str(self.element.text)
            logging.info("Get the text "+data)
            self.step_result = {"text":data,"results":"pass","msg":""}
            
        else:
            self.step_result = {"text":"","results":"fail","msg":"does not found the expected text"}
        
        return self.step_result

class code(): #可执行代码段
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        driver = self.step_data.get("driver")
        self.which = self.step_data.get("which")
        self.what = self.step_data.get("what")
        logging.info(self.which)
        if self.which:
            self.what = self.which.get("code")
        
        time.sleep(2)
        exec(self.what)
        time.sleep(3)
        
        self.step_result={"result":"pass","msg":""}
        return self.step_result

class input_text():
    def __init__(self,step_data):
        self.step_data = step_data
            
    def __call__(self): #输入 参数：输入字符串
        find_class=find(self.step_data)
        self.element=find_class()
            
        if self.element:
            try:
                self.element.click()
                self.driver.set_fastinput_ime(True)
                self.driver.send_keys(self.swhat)
                self.driver.set_fastinput_ime(False)
                logging.info("inputed")
                time.sleep(1)
                self.step_result = {"result":"pass","message":"inputed"}
            except Exception as e:
                print(e)
                self.step_result = {"result":"error","message":"the element does not editable"}
        else:
            self.step_result = {"result":"error","message":"input string is failed!!!"}
        
        return self.step_result

class click(): #滑动
    def __init__(self,step_data):
        self.step_data = step_data
        
    def __call__(self): #点击
        find_class=find(self.step_data)
        self.element=find_class()
            
        if self.element:
            try:
                self.element.click()  #对象点击
                logging.info("clicked")
                time.sleep(1)
                self.step_result = {"result":"pass","message":"clicked"}
            except Exception as e:
                logging.error(e)
                self.step_result = {"result":"error","message":"the element does not clicable"}
        else:
            self.step_result = {"result":"error","message":"the element does not found"}
        
        return self.step_result

class mini_app_click():
    def __init__(self,step_data):
        self.step_data = step_data
        
    def __call__(self):
        self.step_result = {}
        for i in range(5):
            driver=self.step_data.get("driver")
            self.which=self.step_data.get("which")
            self.what=self.step_data.get("what")
            self.testcaseclass=self.step_data.get("class")
            try:
                self.elements = driver(className=u"android.webkit.WebView")  #根据uiautomator 查询对象
            except Exception as e:
                print(e)
        
            for i in range(len(self.elements)):
                try:
                    self.element = self.elements[i]
                    x = self.element.child(className="android.view.View")
                    for j in range(len(x)):
                        try:
                            element = self.element.child(className="android.view.View",instance=j)
                            if self.what in element.info.get("contentDescription"):
                                self.element = element
                                break
                        except Exception as e:
                            logging.error(e)
                    if self.element:
                        break
                except Exception as e:
                    logging.error(e)
        
            if self.element:
                try:
                    self.element.click()  #对象点击
                    logging.info("clicked")
                    time.sleep(1)
                    self.step_result = {"result":"pass","message":"clicked"}
                except Exception as e:
                    logging.error(e)
                    self.step_result = {"result":"error","message":"the element does not clicable"}
            else:
                driver(className="android.widget.ImageButton", instance=3).click()
                time.sleep(3)
                driver(className='android.widget.TextView',text='钱包商家Li…').click()
                time.sleep(3)
        if self.step_result:
            pass
        else:
            self.step_result = {"result":"error","message":"the element does not clicable"}
        return self.step_result

class swipe(): #滑动
    def __init__(self,step_data):
        self.step_data = step_data
       
    def __call__(self):
        logging.info(self.step_data.get("which"))
        self.driver = self.step_data.get("driver")
        swipe_info = eval(self.step_data.get("which").get("swipe"))
        if swipe_info:
            self.x1 = swipe_info[0]
            self.x2 = swipe_info[1]
            self.y1 = swipe_info[2]
            self.y2 = swipe_info[3]
            self.d =  swipe_info[4]
        
        try:
            self.driver.swipe(self.x1,self.y1,self.x2,self.y2,self.d)
        except Exception as e:
            logging.error(e)
            
        logging.info("swipe from "+str(self.x1)+"X"+str(self.y1)+" to "+str(self.x2)+"X"+str(self.y2))
        self.step_result={"result":"pass","msg":""}
        return self.step_result

class check():  #比较页面对象的文本与期望的文本
    def __init__(self,step_data):
        self.step_data = step_data
        self.driver=self.step_data.get("driver")
        self.step_name=self.step_data.get("step_name")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.expected=self.step_data.get("expected")
        self.check_type=self.step_data.get("check_type")
        self.testcaseclass=self.step_data.get("class")
        self.testcase_name=self.step_data.get("testcase_name")
        
    def do(self):
        if self.check_type:
            self.this_check=eval("self."+self.check_type)
        else:
            self.this_check=eval("self.equal")
            logging.warning("Does not select check type,the default is equal")
        self.data={}
        self.step_result=self.this_check()
        return self.step_result
        
    def equal(self):
        #文本精确检查-相同
        text=get_text(self.step_data)
        self.actual = text()
        try:                                                         
            self.testcaseclass.assertEqual(self.actual,self.expected,"The expected text "+self.expected+" does not found in the page - Fail")
            logging.info("The expected text "+self.expected+" is found in the page - Pass")
            self.step_result={"result":"pass","msg":"The expected text "+self.expected+" is found in the page - Pass"}
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The expected text "+self.expected+" does not found in the page - Fail")

        return self.step_result
    
    def notequal(self):
        #文本精确检查 -不相同
        text=get_text(self.step_data)
        self.actual = text()
        try:                                                         
            self.testcaseclass.assertNotEqual(self.actual,self.expected,"The expected text "+self.expected+" is found in the page - Fail")
            logging.info("The expected text "+self.expected+" does not found in the page - Pass")
            self.step_result={"result":"pass","msg":"The expected text "+self.expected+" does not found in the page - Pass"}
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The expected text "+self.expected+" is found in the page - Fail")

        return self.step_result
        
    def like(self):
        #文本模糊检查 - 包含
        text=get_text(self.step_data)
        self.actual = text()
        try:                                                   
            self.testcaseclass.assertIn(self.expected,self.actual,"The expected text "+self.expected+" does not found in the page - Fail")
            logging.info("The expected text "+self.expected+" is found in the page - Pass")
            self.step_result={"result":"pass","msg":"The expected text "+self.expected+" is found in the page - Pass"}
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The expected text "+self.expected+" does not found in the page - Fail")

        return self.step_result
        
    def notlike(self):
        #文本模糊检查 - 不包含
        text=get_text(self.step_data)
        self.actual = text()
        try:                                                         
            self.testcaseclass.assertNotIn(self.expected,self.actual,"The expected text "+self.expected+" is found in the page - Fail")
            logging.info("The expected text "+self.expected+" does not found in the page - Pass")
            self.step_result={"result":"pass","msg":""}
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The expected text "+self.expected+" is found in the page - Fail")

        return self.step_result
    
    def existed(self):
        #根据 xpath 查找对象是否存在 - TRUE = 存在
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if isinstance(self.which,dict):
            for key in self.which:
                self.temp_which=self.which[key]
        try:
            self.testcaseclass.assertTrue(self.element,"The element "+self.temp_which+" does not existed in the page - Fail")
            self.step_result={"result":"pass","msg":""}
            logging.info("The element "+self.temp_which+" is existed in the page - Pass")
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The element "+self.temp_which+" does not existed in the page - Fail")
        logging.info(self.step_result)
        return self.step_result
    
    def notexisted(self):
        #根据 xpath 查找对象是否存在 - TRUE = 不存在
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if isinstance(self.which,dict):
            for key in self.which:
                self.temp_which=self.which[key]
        try:
            self.testcaseclass.assertFalse(self.element,"The element "+self.temp_which+" is existed in the page - Fail")
            self.step_result={"result":"pass","msg":""}
            logging.info("The element "+self.temp_which+" does not existed in the page - Pass")
            
        
        except AssertionError as e:
            self.step_result={"result":"fail","msg":str(e)}
            logging.info("The element "+self.temp_which+" is existed in the page - Fail")
            
        return self.step_result 
###########################################################################
class screen():   #屏幕截图
    def __init__(self,step_data,delay):
        self.step_data = step_data
        self.driver = self.step_data.get("driver")
        self.step_name = self.step_data.get("step_name")
        self.testcaseclass = self.step_data.get("class")
        self.testcase_name = self.step_data.get("testcase_name")
        self.delay = delay 
        
    def do(self):
        time.sleep(self.delay)
        file_name = get_variable().SCREENFOLDER+self.testcase_name+"_"+self.step_name+"_"+time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))+".png"    #输出目录+文件名
        self.driver.screenshot(file_name) #截图并保存

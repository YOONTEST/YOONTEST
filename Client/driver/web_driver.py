# coding=utf8
# author:kang
##############WEB测试驱动#########################################
#1.使用 selenium2.0 webdriver 作为底层驱动
#2.启动 Chrome 浏览器
#3.获取测试用例的测试数据，如：操作，被操作的页面对象，输入输入的内容，断言类型，期望结果。。。
#4.被选择的对象会高亮显示
#5.支持多种操作方法  点击，JS点击，输入，JS输入，获取，上传图片，执行代码，检查断言，屏幕截图。。。
###############################################################

import os,sys,time
from datetime import datetime
import logging
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,WebDriverException,ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import win32gui
import win32con

curPath = os.path.abspath(os.path.dirname(__file__))  
rootPath = os.path.split(curPath)[0]  
sys.path.append(rootPath)

from Client.lib.load_data import test_case
from Client.setting.variable import get_variable

################## 启动CHROME ###############################
class chrome(unittest.TestCase): 
    def launch(self):
        try: 
            chrome_driver=get_variable().CHROME_DRIVER
            logging.debug(chrome_driver)
            web_browser = webdriver.Chrome(executable_path=chrome_driver)
            web_browser.set_page_load_timeout(30)
            web_browser.maximize_window()
            #web_browser.set_window_size(480, 800)
        except WebDriverException as e:
            logging.info(e)
            web_browser=None          
                
        return web_browser
    
    def close(self,driver):
        time.sleep(3)
        driver.close()
        logging.info("driver is closed!!!")
        self.testcase_result={"result":"pass","msg":""}
        return self.testcase_result
    
######################################################
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
        self.test_case_data["step"] = []
        self.test_case_data["driver"] = chrome().launch() #启动浏览器
        start_time=datetime.now()
        
        for one_step in self.test_cases:
            self.step_data={}
            self.step_data["driver"] = self.test_case_data["driver"]
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
        open_class = open(self.step_data)
        self.step_result = open_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def close(self):
        self.step_result= chrome().close(self.driver)
        return self.step_result
    
    def click(self):
        click_class = click(self.step_data)
        self.step_result = click_class()
        screen(self.step_data,3).do
        return self.step_result
        
    def js_click(self):
        js_click_class = js_click(self.step_data)
        self.step_result = js_click_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def input(self):
        input_class = input_text(self.step_data)
        self.step_result = input_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def js_input(self):
        js_input_class = js_input(self.step_data)
        self.step_result = js_input_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def wait(self):
        time.sleep(int(self.test_step_data["what"]))
        logging.info("script waiting for "+str(int(self.test_step_data["what"])))
        self.step_result={"result":"pass","msg":"script waiting for "+str(int(self.test_step_data["what"]))}
        return self.step_result
        
    def check(self):
        self.step_result=check(self.step_data).do()
        return self.step_result
    
    def get_text(self):
        get_text_class = get_text(self.step_data)
        self.step_result = get_text_class()
        return self.step_result
    
    def upload(self):
        upload_class =  upload(self.step_data)
        self.step_result = upload_class()
        screen(self.step_data,3).do()
        return self.step_result
    
    def code(self):
        code_class = code(self.step_data)
        self.step_result = code_class()
        screen(self.step_data,3).do()
        return self.step_result

####################################################################
class open(unittest.TestCase):  #打开URL
    def __init__(self,step_data):
        self.step_data = step_data
        
    def __call__(self):
        self.browser=self.step_data["driver"]
        self.which=self.step_data["which"]
        self.url = self.which.get("url")
        try: 
            self.browser.get(self.url)
            self.step_result={"result":"pass","msg":""}
        except WebDriverException as e:
            logging.info(e)
            self.step_result={"result":"fail","msg":"webdriver error"}
        return self.step_result


class find(): #查找页面对象
    def __init__(self,driver,which,what,testcaseclass):
        self.driver = driver
        self.which = which
        self.what = what
        self.testcaseclass = testcaseclass
        self.element=""
        if isinstance(self.which,dict):
            self.which=self.which.get("xpath")
        self.data={}
            
    def __call__(self):
    #查找一个页面对象          
        for i in range(10):
            try:
                self.element = self.driver.find_element_by_xpath(self.which)
                if (self.element.is_displayed()):
                    self.highligh_element(self.element)
                return self.element
            except NoSuchElementException as e:
                logging.error(e)
            except StaleElementReferenceException as e:
                logging.error(e)
            except AttributeError as e:
                logging.error(e)
            except WebDriverException as e:
                logging.error(e)         
            logging.info("waiting for "+str(i)+" seconds")
            time.sleep(1)
                                   
        if self.element=="":
            logging.warning(self.which+" does not found")
            return False

    def highligh_element(self,element): #高亮显示页面对象
        #高亮显示选择的页面元素
        js = "element = arguments[0];" +"element.scrollIntoView();"
        self.driver.execute_script(js,element)
        js = "element = arguments[0];" +"original_style = element.getAttribute('style');" +"element.setAttribute('style', original_style + \";" +"background: yellow; border: 2px solid red;\");" +"setTimeout(function(){element.setAttribute('style', original_style);}, 1500);"
        self.driver.execute_script(js,element)
        time.sleep(1)
        
class click():   #点击页面对象
   
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        logging.info(self.element)
        
        if isinstance(self.which,dict):
            for key in self.which:
                self.temp_which=self.which[key]
        
        if (self.element!=False):
            try:
                self.element.click()
                logging.info(self.temp_which+" clicked")
                self.step_result={"result":"pass","msg":""}
            except ElementNotVisibleException as e:
                logging.warning(self.temp_which+" does not visible")
                self.step_result={"result":"fail","msg":str(e)}
            except WebDriverException as e:
                logging.warning(self.temp_which+" does not visible")
                self.step_result={"result":"fail","msg": str(e)}
        return self.step_result
    
class js_click(): #点击JS页面对象
    
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if isinstance(self.which,dict):
            for key in self.which:
                self.temp_which=self.which[key]
        
        if (self.element!=False):
            try:
                self.element.click()
                logging.info(self.temp_which+" clicked")
                self.step_result={"result":"pass","msg":""}
                            
            except ElementNotVisibleException as e:
                    logging.warning(self.temp_which+" does not visible1")
                    self.step_result={"result":"fail","msg":str(e)}
            except WebDriverException as e:
                    logging.warning(self.temp_which+" does not visible1")
                    self.step_result={"result":"fail","msg":str(e)}
        return self.step_result

class input_text(): #键盘输入
    
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if (self.element!=False): 
            try:
                self.element.clear()
                
                if "{enter}" in self.what:
                    self.what = str(self.what).replace("{enter}","")
                    self.element.send_keys(str(self.what))
                    self.element.send_keys(Keys.ENTER)
                else:
                    self.element.send_keys(str(self.what))
                    
                logging.info("Inputed "+ str(self.what)+" in the box")
                self.step_result={"result":"pass","msg":""}

            except ElementNotVisibleException:
                logging.warning("the element can not be visible")
                self.step_result={"result":"fail","msg":"the element can not be visible"}
        
            except WebDriverException:
                logging.warning("driver error")
                self.step_result={"result":"fail","msg":"driver error"}
        return self.step_result

class js_input(): #键盘输入到JS控件
    
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if (self.element!=False): 
            try:
                
                actions = webdriver.ActionChains(self.brwoser)
                actions.move_to_element(self.element)
                actions.click()
                time.sleep(1)
                if "{enter}" in self.what:
                    self.what = str(self.what).replace("{enter}","")
                    actions.send_keys(self.what)
                    self.element.send_keys(Keys.ENTER)
                else:
                    actions.send_keys(self.what)
                actions.perform()
                
                logging.info("Inputed "+ str(self.what)+" in the box")
                self.step_result={"result":"pass","msg":""}

            except ElementNotVisibleException:
                logging.warning("the element can not be visible")
                self.step_result={"result":"fail","msg":"the element can not be visible"}
        
            except WebDriverException as e:
                logging.warning(e)
                self.step_result={"result":"fail","msg":"driver error"}
        return self.step_result

class get_text(): #根据 xpath 查找对象，并获取文本 
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
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
    

class upload():  #上传本地文件
    def __init__(self,step_data):
        self.step_data = step_data

    def __call__(self):
        self.driver=self.step_data.get("driver")
        self.which=self.step_data.get("which")
        self.what=self.step_data.get("what")
        self.testcaseclass=self.step_data.get("class")
        
        find_class=find(self.driver,self.which,self.what,self.testcaseclass)
        self.element=find_class()
        
        if isinstance(self.which,dict):
            for key in self.which:
                self.temp_which=self.which[key]
                
        if (self.element!=False):
            self.i=0
            for self.i in range(11):
                try:
                    time.sleep(5)
                    self.element.click()
                    logging.info(self.temp_which+" clicked")
                    time.sleep(2)
                    # win32gui
                    dialog = win32gui.FindWindow('#32770', u'打开')                               # 对话框
                    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None) 
                    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
                    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)                     # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
                    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)                   # 确定按钮Button

                    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, self.what)            # 往输入框输入绝对地址
                    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)                # 按button
                    time.sleep(2)
                    self.step_result={"result":"pass","msg":""}
                    break
                            
                except ElementNotVisibleException:
                    if self.i>=10:
                        logging.warning(self.temp_which+" does not visible")
                        self.step_result[self.step_name]={"result":"fail","msg":self.temp_which+" does not visible"}
                        return False
                except WebDriverException:
                    if self.i>=10:
                        logging.warning(self.temp_which+" does not visible")
                        self.step_result[self.step_name]={"result":"fail","msg":self.temp_which+" does not visible"}
                        return False
                time.sleep(1)
                
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
class screen():
    def __init__(self,step_data,delay):
        self.step_data = step_data
        self.driver = self.step_data.get("driver")
        self.step_name = self.step_data.get("step_name")
        self.testcaseclass = self.step_data.get("class")
        self.testcase_name = self.step_data.get("testcase_name")
        self.delay = delay 
    def do(self):
        #web 测试截图
        time.sleep(self.delay)
        self.driver.get_screenshot_as_file(get_variable().SCREENFOLDER+self.testcase_name+"_"+time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))+".png")

# coding=utf8
# author:kang
# 百度API
from aip import AipOcr
import json
from PIL import Image
 
class baidu_api():
    #百度API调用
    def __init__(self):
        # 定义常量
        self.APP_ID = '11462932'
        self.API_KEY = 'P2ybUvst8AaDI3ZugmZMYTdG'
        self.SECRET_KEY = 'uAfid2CG0mxPwzXHKBekcocPLow1z9cf'
        # 初始化AipFace对象
        self.aipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        # 定义参数变量
        self.options = {'detect_direction': 'true','language_type': 'CHN_ENG',}
    
    def get_text(self,filePath):
        # 调用通用文字识别接口
        result = self.aipOcr.basicGeneral(self.get_file_content(filePath), self.options)
        x=eval(json.dumps(result))
        return x
    
    def get_text_with_location(self,filePath):
        # 调用通用文字识别接口
        result = self.aipOcr.general(self.get_file_content(filePath), self.options)
        x=eval(json.dumps(result))
        print(x)
        return x
        
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

class txt_coordinate():
    def __init__(self):
        pass
    def do(self,path,file,expect):
        baidu_json = baidu_api().get_text_with_location(path+file)
        actual_list = baidu_json.get("words_result")
        data = {}
        for i in range(len(actual_list)):
            actual = baidu_json.get("words_result")[i].get("words")
            location = baidu_json.get("words_result")[i].get("location")
            if expect in actual:
                if expect == actual:
                    data["result"]="true"
                    data["coordinate"]=location
                else:
                    data["result"]="true"
                    data["coordinate"]=location
                        
        if data.get("result")!="true":
            data["result"]="false"
            data["coordinate"]={}
            
        return data

class verify_text():
    #检查文本
    def __init__(self):
        pass
    
    def do(self,path,file,expect):
        baidu_json = baidu_api().get_text(path+file)
        data = {}
        if baidu_json:
            if baidu_json.get("words_result_num") == 1:
                actual = baidu_json.get("words_result")[0].get("words")
                if expect in actual:
                    if expect == actual:
                        data["result"]="true"
                        data["message"]="精确找到文本 "+expect
                        data["status"]="1"   #只有一个结果，并且精确匹配
                    else:
                        data["result"]="true"
                        data["message"]="找到包含字符串的文本 "+expect
                        data["status"]="2"   #只有一个结果，模糊匹配
                else:
                    data["result"]="false"
                    data["message"]="没有找到文本 "+expect
                    data["status"]="0" #没有结果
            else:
                actual_list = baidu_json.get("words_result")
                for i in range(len(actual_list)):
                    actual = baidu_json.get("words_result")[i].get("words")
                    if expect in actual:
                        if expect == actual:
                            data["result"]="true"
                            data["message"]="列表中找到文本 "+expect
                            data["status"]="3"  #多个结果，精确匹配
                        else:
                            data["result"]="true"
                            data["message"]="列表中找到包含字符串的文本 "+expect
                            data["status"]="4"  #多个结果，模糊匹配
                        
                if data.get("result")!="true":
                    data["result"]="false"
                    data["message"]="列表中没有找到文本 "+expect
                    data["status"]="0"  #没有结果
                    
        return data

class cut_image():
    def __init__(self):
        pass
    
    def rate(self,path,from_file,to_file,size):
        img = Image.open(path+from_file)
        high = int(img.size[0])
        width = int(img.size[1])
        
        start_x=high*size[0]/100
        start_y=width*size[1]/100
        end_x=high*size[2]/100
        end_y=width*size[3]/100
        
        rangle = (start_x,start_y,end_x,end_y)
        
        jpg = img.crop(rangle)
        jpg.save(path+to_file)
        return {"result":"true","message":"按比率图片截取成功!","path":path+to_file}
        
    def coordinate(self,path,from_file,to_file,size):
        img = Image.open(path+from_file)   
        jpg = img.crop(size)
        jpg.save(path+to_file)
        return {"result":"true","message":"按坐标图片截取成功!","path":path+to_file}

#print(cut_image().rate("C:\\Users\\dell\\Desktop\\","1.jpg","2.jpg",(0,0,50,50)))
#print(cut_image().coordinate("C:\\Users\\dell\\Desktop\\","1.jpg","3.jpg",(0,0,50,50)))
#print(verify_text().do("C:\\Users\\dell\\Desktop\\","1.jpg","*门店名称:文豪家的店648"))
#print(txt_coordinate().do("C:\\Users\\dell\\Desktop\\","1.jpg","*门店名称:文豪家的店648"))

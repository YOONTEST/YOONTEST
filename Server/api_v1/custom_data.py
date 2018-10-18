#coding=utf-8
# author:kang
# 获取自定义数据
import time
import datetime
import pymysql.cursors
import urllib
import os,sys
from datetime import datetime
from bson import json_util as jsonb
import random
import requests
from pymongo import MongoClient

#===================数据库配置=================================
class MONGO_DB:
    def __init__(self):
        self.DB_NAME="mongodb://118.31.48.228:27116/"

    def conn(self):
        client = MongoClient(self.DB_NAME)
        return client


#===================方法=======================================
class getdata():
#--generate random data--------------------------------
    def between(self,_str,_s,_e):
        return _str[_str.index(_s)+len(_s):_str.index(_e)]

    def random_number(self,m):#返回随机数
        s=1
        e=10**int(m)-1
        result = str(random.randint(s,e))
        return result

    def random_int(self,m):#返回指定位数的随机数
        s=10**(int(m)-1)
        e=10**int(m)-1
        result = str(random.randint(s,e))
        return result
    
    def random_str(self,m):#返回自定个数的随机字符串
        seed = "abcdefghijklmnopqrstuvwxyz"
        sa = []
        for i in range(m):
            sa.append(self.choice(seed))
        result = ''.join(sa)
        return result
    
    def random_mobile(self):#返回随机手机号
        result = "13"+str(self.random_int(9))
        return result
    
    def random_email(self):#返回随机邮件
        result = "qbemail@"+self.random_str(4)+".com"
        return result

    def random_longitude_and_latitude(self):#返回指定位数的随机数
        s = 10**(int(12)-1)
        e = 10**int(12)-1
        long_s = "121."
        lat_s = "31."
        long_m = str(random.randint(67,97))
        lat_m = str(random.randint(0,31))
        long_e = str(random.randint(s,e))
        lat_e = str(random.randint(s,e))
        longitude = long_s+long_m+long_e
        latitude = lat_s+lat_m+lat_e
        result = {"longitude":longitude,"latitude":latitude}
        return result

    def mini_apps_token(self,data):  # auth 包括手机号密码
        auth_user = data["user"]
        auth_password = data["password"]
        loginid = auth_user  #手机号
        loginpwd = auth_password #密码
        which = "https://sc.qianbaocard.org/api/sc/v1/user/login"
        what = {"username":loginid,"password":loginpwd}
        headers = {"Content-Type":"application/json"}
        try:
            autho_request = requests.post(which,headers=headers,json=what,verify=False)
            result = autho_request.json()
            if result.get("message") == "成功":
                return "bearer " + result.get("data").get("accessToken")
            else:
                return ""
        except:
            return ""

    def vinci_token(self,data):  # auth 包括手机号密码
        print("===============================")
        auth_user = data["user"]
        auth_password = data["password"]
        loginid = auth_user  #手机号
        loginpwd = auth_password #密码
        which = "https://vinci-api-test.qianbaocard.org/uc/v1/auth/login"
        what = {'account':loginid, 'password':loginpwd,'needUserInfo':'false'}
        headers = {"Content-Type":"application/json"}
        try:
            autho_request = requests.post(which,headers=headers,json=what,verify=False)
            result = autho_request.json()
            if result.get("message") == "成功":
                return "bearer " + result.get("data").get("accessToken")
            else:
                return ""
        except:
            return ""

    def shop_by_name(self,shop_name,branch_name):  #根据商户名获取店铺ID

        shop_name = shop_name
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_shop
        try:
            results = {"data":str(collection.find_one({'name':shop_name,'branch_name':branch_name})["_id"])}
        except TypeError:
            results = {"data":"","message":"not found shop info"}
        return results["data"]

    def place_by_name(self,place_name):  #根据商户名获取店铺ID

        place_name = place_name
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_place
        try:
            results = {"data":str(collection.find_one({'name':place_name})["_id"])}
        except TypeError:
            results = {"data":"","message":"not found place info"}
        return results["data"]

    def seller_by_name(self,seller_name): #根据商户名获取商户ID
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_seller
        try:
            results = {"data":str(collection.find_one({"name":seller_name})["_id"])}
        except TypeError:
            results = {"data":""}
        return results["data"]

    def qrcode_by_name(self,seller_name):  #根据商户名获取店铺ID
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_qr_code
        try:
            results = {"data":str(collection.find_one({"seller.name":seller_name,"target.eid":""})['sn'])}
        except TypeError:
            results = {"data":""}
        return results["data"]

    def get_qrcode(self,seller_name):  #根据商户名获取店铺ID
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_qr_code
        try:
            results = {"data":str(collection.find_one({"seller.name":seller_name,"target.eid":""})['sn'])}
        except TypeError:
            results = {"data":""}
        return results

    def catalog_by_name(self,seller_name,catalog_name):  #根据门店名,分店名 和 类别名 获取类别ID
        seller_name = seller_name
        catalog_name = catalog_name

        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_seller
        try:
            sellerid = str(collection.find_one({"name":seller_name})["_id"])
        except TypeError:
            sellerid = ""

        db = client.vinci_bc
        collection = db.vinci_bc_catalog
        try:
            results = {"data":str(collection.find_one({'seller_id':sellerid,'name':catalog_name})["_id"])}
        except TypeError:
            results = {"data":"","message":"not found catalog info"}
        return results["data"]

    def product_by_name(self,shop_name,branch_name,product_name):  #根据门店名,分店名,商品名获取商品ID
        shop_name = shop_name
        branch_name = branch_name
        product_name = product_name
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_product
        try:
            results = {"data":str(collection.find_one({'shop.name':shop_name,'shop.branch_name':branch_name,'name':product_name})["_id"])}
        except TypeError:
            results = {"data":"","message":"not found catalog info"}
        return results["data"]

    def printer_by_name(self,shop_name,branch_name,printer_name):  #根据门店名,分店名,商品名获取商品ID
        shop_name = shop_name
        branch_name = branch_name
        printer_name = printer_name
        client = MONGO_DB().conn()
        db = client.vinci_bc
        collection = db.vinci_bc_printer
        try:
            results = {"data":str(collection.find_one({'shop.name':shop_name,'shop.branch_name':branch_name,'name':printer_name})["_id"])}
        except TypeError:
            results = {"data":"","message":"not found printer info"}
        print("I am here!!!!!!!!!!!!!!!!!!!!!")
        print(results)
        return results["data"]

    def wifi_by_ssid(self,shop_name,branch_name,ssid):  #根据商户名获取店铺ID

        shop_name = shop_name
        branch_name = branch_name
        ssid = ssid
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_shop
        try:
            wifis = collection.find_one({'name':shop_name,'branch_name':branch_name,'wifi_devices.ssid':ssid})["wifi_devices"]
            for wifi in range(len(wifis)):
                if wifis[wifi].get("ssid") == ssid:
                    results = {"data":str(wifis[wifi].get("eid"))}
        except TypeError:
            results = {"data":"","message":"not found shop info"}

        return results["data"]

    def content_by_title(self,seller_name,title):  #根据商户名获取专题，横幅ID
        seller_name = seller_name
        title = title
        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_seller
        try:
            sellerid = str(collection.find_one({"name":seller_name})["_id"])
        except TypeError:
            sellerid = ""

        db = client.vinci_cc
        collection = db.vinci_cc_content
        try:
            results = {"data":str(collection.find_one({'seller_id':sellerid,'title':title})["_id"])}
            print(results)
        except TypeError:
            results={"data":"","message":"not found content info"}
        return results["data"]

    def activity_by_nick_name(self,seller_name,nick_name):  #根据商户名,微信名获取活动id
        seller_name=seller_name
        nick_name=nick_name
        client=MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_seller
        try:
            sellerid = str(collection.find_one({"name":seller_name})["_id"])
        except TypeError:
            sellerid = ""
        db = client.vinci_mc
        collection = db.vinci_mc_activity
        try:
            results = {"data":str(collection.find({'owner.nick_name':nick_name,'seller_id':sellerid}).sort('created_time',-1)[0]["_id"])}
        except TypeError:
            results = {"data":"","message":"not found content info"}
        return results["data"]

    def item_by_nick_name(self,seller_name,nick_name,item_name):  #根据商户名,微信名获取活动id
        seller_name = seller_name
        nick_name = nick_name
        item_name = item_name

        client = MONGO_DB().conn()
        db = client.vinci_sc
        collection = db.vinci_sc_seller
        try:
            sellerid = str(collection.find_one({"name":seller_name})["_id"])
        except TypeError:
            sellerid = ""
        db = client.vinci_mc
        collection = db.vinci_mc_activity
        try:
            list = collection.find({'owner.nick_name':nick_name,'seller_id':sellerid}).sort('created_time',-1)[0]['items']
            for i in range(len(list)):
                if list[i].get("name") == item_name:
                    results = {"data":list[i].get("eid")}
                    print(results)
        except TypeError:
            results = {"data": "", "message": "not found content info"}

        return results["data"]

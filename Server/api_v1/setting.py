#coding=utf-8
# author:kang
# 设置数据接口
from django.http import JsonResponse
from sign.models import Key_repository
import os,time,urllib
from django.core import serializers

#获取设配数据
def get(request):
    key_name = request.GET.get('key_name','')
    key_name=urllib.request.unquote(key_name)

    setting = Key_repository.objects.filter(key_name=key_name)
    key_value = ""
    for one in setting:
        key_value = one.key_value

    return JsonResponse({key_name:key_value})

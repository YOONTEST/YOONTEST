#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Device
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import os
import time
import urllib
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
logger = logging.getLogger(__name__)


# 用例管理
@login_required
def device(request):
    device_list = Device.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(device_list, 10)
    page = request.GET.get('page')
    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        devices = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        devices = paginator.page(paginator.num_pages)

    return render(request, "device.html", {"user": username,"devices":devices})

# 用例管理
@login_required
def add_device(request):
    username = request.session.get('username', '')
    return render(request, "add_device.html", {"user": username,"device":""})

@login_required
def add_device_action(request):
    username = request.session.get('username', '')
    device_id = request.POST.get('device_id','')       # 用例集名
    name = request.POST.get('name','')       # 用例集名
    app_name = request.POST.get('app_name','')       # 用例集名
    device_info = request.POST.get('device_info','')       # 用例集名

    element = Device.objects.filter(app_name =app_name,name=name)
    if len(element):
        return HttpResponseRedirect('/device/')
    if name=="":
        return HttpResponseRedirect('/device/')
    else:
        Device.objects.create(name=name,app_name=app_name,device_info=device_info)
    return HttpResponseRedirect('/device/')

# 用例管理
@login_required
def edit_device(request,device_id):
    device = Device.objects.filter(id=device_id)
    username = request.session.get('username', '')
    return render(request, "add_device.html", {"user": username,"device":device})

@login_required
def view_device(request,device_id):
    device = Device.objects.filter(id=device_id)
    username = request.session.get('username', '')
    return render(request, "view_element.html", {"user": username,"device":device})

# 用例管理
@login_required
def edit_device_action(request):
    username = request.session.get('username', '')
    device_id = request.POST.get('device_id','')       # 用例集名
    name = request.POST.get('name','')       # 用例集名
    app_name = request.POST.get('app_name','')       # 用例集名
    device_info = request.POST.get('device_info','')       # 用例集名


    device = Device.objects.filter(id=device_id)

    device.update(name=name,app_name=app_name,device_info=device_info)
    return HttpResponseRedirect('/device/')

# 用例管理
@login_required
def delete_device_action(request,device_id):
    username = request.session.get('username', '')
    device = get_object_or_404(Device, id=device_id)
    element = Device.objects.filter(id=device_id)
    element.delete()
    return HttpResponseRedirect('/device/')

# 用例名称搜索
@login_required
def search_contents_device(request):
    username = request.session.get('username', '')
    search_contents = request.GET.get("contents", "")
    #search_contents_bytes = search_contents.encode(encoding="utf-8")
    search_contents_bytes=search_contents
    device_lists = Device.objects.filter(deviceName__contains=search_contents_bytes)
    paginator = Paginator(device_lists, 10)
    page = request.GET.get('page')
    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        devices = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        devices = paginator.page(paginator.num_pages)

    return render(request, "repository.html", {"user": username, "devices": devices})


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

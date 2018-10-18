#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Repository,Teststep
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
def repositories(request):
    elements = Repository.objects.all().order_by("key")
    username = request.session.get('username', '')

    paginator = Paginator(elements,20)
    page = request.GET.get('page')
    try:
        element_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        element_list = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        element_list = paginator.page(paginator.num_pages)

    return render(request, "repository.html", {"user": username,"element_list":element_list})

# 用例管理
@login_required
def element(request,action,element_key):
    username = request.session.get('username', '')
    key = request.POST.get('key','')       # 用例集名
    find_by = request.POST.get('find_by','')       # 用例集名
    find_by_value = request.POST.get('find_by_value','')       # 用例集名
    app = request.POST.get('app','')       # 用例集名
    platform = request.POST.get('platform','')       # 用例集名

    temp_element = Repository.objects.filter(key=element_key)
    element_id=0
    for ele in temp_element:
        element_id=ele.id
    element = Repository.objects.filter(id=element_id)

    if action=='view':
        if element_key=='0':
            return render(request, "element.html", {"user": username,"element":""})
        else:
            element = Repository.objects.filter(id=element_id)
            return render(request, "element.html", {"user": username,"element":element,"readonly":'True'})
    if action=='edit':
        element = Repository.objects.filter(id=element_id)
        return render(request, "element.html", {"user": username,"element":element})
    elif action=="add":
        if len(element):
            old_key=""
            for old in element:
                old_key=old.key

            element.update(key=key,find_by=find_by,app=app,platform=platform,find_by_value=find_by_value)

            steps = Teststep.objects.filter(which=old_key)
            for step in steps:
                one_step = Teststep.objects.filter(id=step.id)
                one_step.update(which=key,case_id=step.case_id,step_name=step.step_name,how=step.how,what=step.what,expected=step.expected,check_type=step.check_type)

            return HttpResponseRedirect('/repository/')
        else:
            ele = Repository.objects.filter(key=key)
            if len(ele):
                return HttpResponseRedirect('/repository/')
            if key=="":
                return HttpResponseRedirect('/repository/')
            else:
                Repository.objects.create(key=key,find_by=find_by,app=app,platform=platform,find_by_value=find_by_value)
            return HttpResponseRedirect('/repository/')

    elif action=="delete":
        element.delete()
        return HttpResponseRedirect('/repository/')

# 用例名称搜索
@login_required
def search_contents_element(request):
    username = request.session.get('username', '')
    search_contents = request.GET.get("contents", "")
    #search_contents_bytes = search_contents.encode(encoding="utf-8")
    search_contents_bytes=search_contents
    element_list = Repository.objects.filter(key__contains=search_contents_bytes)

    paginator = Paginator(element_list, 10)
    page = request.GET.get('page')
    try:
        elements = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        elements = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        elements = paginator.page(paginator.num_pages)

    return render(request, "repository.html", {"user": username, "elements": elements})


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

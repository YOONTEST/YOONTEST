#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Testcase,Test_plan,Device,Repository,Plan_case,Reportlist,Execution,Device
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
from django.core import serializers
logger = logging.getLogger(__name__)


# 用例名称搜索
@login_required
def search_case(request,platform,search_contents):
    username = request.session.get('username', '')
    list=""
    if platform=="app":
        list1 = Testcase.objects.filter(testcase_name__contains=search_contents,platform="ios").order_by("testcase_name")
        list2 = Testcase.objects.filter(testcase_name__contains=search_contents,platform="android").order_by("testcase_name")
        list = list1 | list2
    else:
        list = Testcase.objects.filter(testcase_name__contains=search_contents,platform=platform).order_by("testcase_name")

    paginator = Paginator(list, 20)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "case.html", {"user": username,"platform":platform,"test_case": items})


def search_plan(request, search_contents):
    username = request.session.get('username', '')
     #list = Testcase_api.objects.filter(testcase_name__contains=search_contents_bytes)
    list = Test_plan.objects.filter(plan_name__contains=search_contents).order_by("plan_name")
    paginator = Paginator(list, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
         # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "test_plan.html", {"user": username, "test_plan": items})

def search_device(request, search_contents):
    username = request.session.get('username', '')
    #list = Testcase_api.objects.filter(testcase_name__contains=search_contents_bytes)
    list = Device.objects.filter(name__contains=search_contents).order_by("id")
    paginator = Paginator(list, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "device.html", {"user": username, "devices": items})

def search_element(request, search_contents):
    username = request.session.get('username', '')
    #list = Testcase_api.objects.filter(testcase_name__contains=search_contents_bytes)
    list = Repository.objects.filter(key__contains=search_contents).order_by("id")
    paginator = Paginator(list, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "repository.html", {"user": username, "element_list": items})

def search_plan_details(request,plan_id,search_contents):
    username = request.session.get('username', '')
    list = plan_case.objects.filter(testcase_name__contains=search_contents).order_by("id")
    #print(serializers.serialize("json", list))

    paginator = Paginator(list, 20)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "caseplan-detail.html", {"user": username,"test_plan": items,'plan_id':plan_id})


def search_plan_relation(request,plan_id,search_contents):
    username = request.session.get('username', '')
    list = Testcase_api.objects.filter(testcase_name__contains=search_contents,status='1').order_by("id")
    #print(serializers.serialize("json", list))

    paginator = Paginator(list, 20)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        items = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        items = paginator.page(paginator.num_pages)
    return render(request, "CasePlanRelation.html", {"user": username,"test_case": items,'plan_id':plan_id})


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

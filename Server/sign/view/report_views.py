#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Testcase,Execution,Test_plan,Activity,Key_repository,Reportlist,Execution,Device
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

#report测试报告下载方法
@login_required
def report_download(request,type):
    project_name=urllib.request.unquote(project_name)
    with open("..\\Result\\api\\report\\"+project_name+".html") as f:
        c = f.read()
    return HttpResponse(c)

# 报告管理
@login_required
def report(request,type):
    username = request.session.get('username', '')
    app_report = Activity.objects.filter(test_type='APP')
    app_count=str(len(app_report))
    api_report = Activity.objects.filter(test_type='API')
    api_count = str(len(api_report))
    web_report = Activity.objects.filter(test_type='WEB')
    web_count = str(len(web_report))
    all_report = Activity.objects.all()
    all_count = str(len(all_report))
    report_list = ""
    activities = ""
    if type =="app" or type=="api" or type=="web":
        report_list = Activity.objects.filter(test_type=type).values("plan_name").distinct()
        activities = Activity.objects.filter(test_type=type)
    elif type=="all":
        activities = Activity.objects.all()
    else:
        plan_name=type
        activities = Activity.objects.filter(plan_name=plan_name)
        types = Test_plan.objects.filter(plan_name=plan_name)
        type=""
        for one_type in types:
            type = one_type.test_type

        report_list = Activity.objects.filter(test_type=type).values("plan_name")

    return render(request, "report.html", {"user": username,"app_count":app_count,"api_count":api_count,"web_count":web_count,"all_count":all_count,'report_list':report_list,'type':type,'activities':activities})


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

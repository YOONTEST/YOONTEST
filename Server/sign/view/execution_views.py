#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Test_plan,Slaves_logs,Activity,Slaves,Execution,Device
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import os,sys
import time
import urllib
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
logger = logging.getLogger(__name__)


# 执行脚本
@login_required
def execution(request):
    plan_list = Test_plan.objects.all().order_by('plan_name')
    slaves = Slaves.objects.all()
    devices = Device.objects.all()
    if len(slaves)==0:
        slave_msg="没有可用主机..."
    else:
        slave_msg="请选择一台主机..."
    
    if len(devices)==0:
        device_msg="没有可用设备..."
    else:
        device_msg="请选择一台设备..."
    username = request.session.get('username', '')
    activity = Activity.objects.all().order_by('-id')

    paginator = Paginator(activity, 10)
    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        activities = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        activities = paginator.page(paginator.num_pages)
    return render(request, "execution.html", {"user": username, "slaves": slaves,"devices":devices,"plan_list":plan_list,"activities": activities,"slave_msg":slave_msg,"device_msg":device_msg})

@login_required
def rerun_scripts(request,activity_id):
    username = request.session.get('username', '')
    current_activity = Activity.objects.filter(id=activity_id)
    all_activity = Activity.objects.all()
    slave_name=""
    for activity in all_activity:
        slave_name=activity.slave_name
    pending_activity = Activity.objects.filter(slave_name=slave_name,status='pending')
    running_activity = Activity.objects.filter(slave_name=slave_name,status='running')

    if len(pending_activity):
        return HttpResponseRedirect('/execution/')
    if len(running_activity):
        return HttpResponseRedirect('/execution/')

    current_activity.update(status='pending')
    return HttpResponseRedirect('/execution/')

@login_required
def delete_scripts(request,activity_id):
    username = request.session.get('username', '')
    current_activity = Activity.objects.filter(id=activity_id)
    current_activity.delete()
    return HttpResponseRedirect('/execution/')

@login_required
def run_scripts(request):
    username = request.session.get('username', '')

    planname = request.GET.get("planname", "")
    slavename = request.GET.get("slavename", "")
    devicename = request.GET.get("devicename", "")
    plan_list = Test_plan.objects.filter(plan_name=planname)
    test_type=""
    for plan in plan_list:
        test_type=plan.test_type

    pending_activity = Activity.objects.filter(slave_name=slavename,status='pending')
    running_activity = Activity.objects.filter(slave_name=slavename,status='running')

    if len(pending_activity):
        return HttpResponseRedirect('/execution/')
    if len(running_activity):
        return HttpResponseRedirect('/execution/')

    if slavename=="" or planname=="" or test_type=="":
        return HttpResponseRedirect('/execution/')
    else:
        Activity.objects.create(plan_name=planname,slave_name=slavename,device_name=devicename,test_type=test_type,status='pending')

    activities = Activity.objects.all()
    return HttpResponseRedirect('/execution/')

@login_required
def run_results(request,activity_id):
    username = request.session.get('username', '')
    execution_all = Execution.objects.filter(activity_id=activity_id).order_by('-endtime')
    test_type = Activity.objects.filter(id=activity_id).values("test_type")[0].get("test_type")
    pass_count=0
    fail_count=0
    error_count=0
    total_count=len(execution_all)
    for i in execution_all:
        if i.casestatus=="pass":
            pass_count = pass_count+1
        if i.casestatus=="fail":
            fail_count = fail_count+1
        if i.casestatus=="error":
            error_count = error_count+1

    paginator = Paginator(execution_all, 5)
    page = request.GET.get('page')
    try:
        executions = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        executions = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        executions = paginator.page(paginator.num_pages)
    return render(request, "run_results.html", {"user": username, "executions": executions,"test_type":test_type,"pass_count":pass_count,"fail_count":fail_count,"error_count":error_count,"total_count":total_count})



'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

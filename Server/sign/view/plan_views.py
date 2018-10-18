#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
from sign.models import Test_plan,Plan_case,Testcase,Device
from django.core import serializers
logger = logging.getLogger(__name__)


#通过 id 筛选删除plan
@login_required
def delete_test_plan_action(request,plan_id):
    username = request.session.get('username', '')
    #test_case = get_object_or_404(test_plan, id=id)
    case = Test_plan.objects.filter(id=plan_id)
    case1=Plan_case.objects.filter(plan_id=plan_id)
    case.delete()
    case1.delete()
    #case_list = test_plan.objects.all()
    return HttpResponseRedirect('/test-plan/')

#通过 plan_id 筛选 删除 Relation关联
@login_required
def delete_CasePlanRelation_action(request,plan_id):
    username = request.session.get('username', '')
    case = Plan_case.objects.filter(plan_id=plan_id)
    case.delete()
    url = '/caseplan-detail/'+plan_id+'/'
    return HttpResponseRedirect(url)

#通过 id 筛选 单条删除 Relation关联
@login_required
def delete_CasePlanRelation_action_s(request,id,plan_id):

    username = request.session.get('username', '')
    #test_case = get_object_or_404(plan_case, id=id)
    case = Plan_case.objects.filter(case_id=id,plan_id=plan_id)
    case.delete()
    url='/caseplan-detail/'+plan_id+'/'
    return HttpResponseRedirect(url)


@login_required
def edit_test_plan_action(request):
    username = request.session.get('username', '')
    plan_id = request.POST.get('plan_id','')
    plan_name = request.POST.get('plan_name','')     # 测试计划名
    test_type = request.POST.get('test_type','')      # 执行次数
    case = Test_plan.objects.filter(id=plan_id)
    case.update(plan_name =plan_name,test_type=test_type)
    return HttpResponseRedirect('/test-plan/')

@login_required
def edit_test_plan(request,plan_id):
    case = Test_plan.objects.filter(id=plan_id)
    username = request.session.get('username', '')
    device_list = Device.objects.all()
    return render(request, "add_test_plan.html", {"user": username,"test_case":case,"device_list":device_list})


@login_required
def view_test_plan(request,plan_id):
    case = Test_plan.objects.filter(id=plan_id)
    username = request.session.get('username', '')
    return render(request, "view_test_plan.html", {"user": username,"test_case":case})

@login_required
def add_test_plan_action(request):
    username = request.session.get('username', '')
    plan_name = request.POST.get('plan_name','')     # 测试计划名
    test_type = request.POST.get('test_type','')
    case = Test_plan.objects.filter(plan_name =plan_name)
    if len(case):
        return HttpResponseRedirect('/test-plan/')
    if plan_name=="":
        return HttpResponseRedirect('/test-plan/')
    case.create(plan_name =plan_name,test_type=test_type)
    return HttpResponseRedirect('/test-plan/')

@login_required
def add_test_plan(request):
    username = request.session.get('username', '')
    device_list = Device.objects.all()
    return render(request, "add_test_plan.html", {"user": username,"test_case":"","device_list":device_list})

@login_required
def Case_checkbox(request,plan_id):
    test_type = Test_plan.objects.filter(id=plan_id).values("test_type")[0].get("test_type")
    if test_type=="API":
        case_list = Testcase.objects.filter(platform='api').order_by('scenario_name','testcase_name')
    elif test_type=="WEB":
        case_list = Testcase.objects.filter(platform='web').order_by('scenario_name','testcase_name')
    elif test_type=="APP":
        case_android = Testcase.objects.filter(platform = 'android').order_by('scenario_name','testcase_name')
        case_ios = Testcase.objects.filter(platform = 'ios').order_by('scenario_name','testcase_name')
        case_list = case_android | case_ios
        
    else:
        case_list = ""

    username = request.session.get('username', '')

    paginator = Paginator(case_list, 30)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)
    return render(request, "CasePlanRelation.html", {"user": username,"test_case":cases,'plan_id':plan_id,'test_type':test_type})

@login_required
def Case_checkbox_submit(request,plan_id):
    url='/edit_PlanRelation/'+plan_id+'/'
    case_list=request.GET.get("case_list")
    cases = case_list.split("_")
    test_type = Test_plan.objects.filter(id=plan_id).values("test_type")[0].get("test_type")

    for the_case_id in cases:
        #scenario_name,testcase_name
        if test_type=="API":
            scenario_name=Testcase.objects.filter(id=the_case_id).values('scenario_name').first()['scenario_name']
            testcase_name=Testcase.objects.filter(id=the_case_id).values('testcase_name').first()['testcase_name']
        elif test_type=="WEB":
            scenario_name=Testcase.objects.filter(id=the_case_id).values('scenario_name').first()['scenario_name']
            testcase_name=Testcase.objects.filter(id=the_case_id).values('testcase_name').first()['testcase_name']
        elif test_type=="APP":
            scenario_name=Testcase.objects.filter(id=the_case_id).values('scenario_name').first()['scenario_name']
            testcase_name=Testcase.objects.filter(id=the_case_id).values('testcase_name').first()['testcase_name']
        #print(plan_id,the_case_id)
        caseid_exist = Plan_case.objects.filter(case_id=the_case_id,plan_id=plan_id)
        if len(caseid_exist):
            pass
            #print(len(caseid_exist))
            #
        else:
            Plan_case.objects.create(plan_id=plan_id, case_id=the_case_id, scenario_name= scenario_name,testcase_name=testcase_name)

    return HttpResponseRedirect(url)

@login_required
def test_plan(request):
    plan_list = Test_plan.objects.all().order_by('plan_name')
    username = request.session.get('username', '')
    paginator = Paginator(plan_list, 10)
    page = request.GET.get('page')
    try:
        plans = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        plans = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        plans = paginator.page(paginator.num_pages)
    #print('z1', plans.plan_id)
    #print('z3', plans.id)

    return render(request, "test_plan.html", {"user": username,"test_plan":plans})

@login_required
def caseplan_detail(request,plan_id):
    mapping_list = Plan_case.objects.filter(plan_id=plan_id).order_by("testcase_name")
    test_type = Test_plan.objects.filter(id=plan_id).values("test_type")[0].get("test_type")
    username = request.session.get('username', '')
    paginator = Paginator(mapping_list, 20)
    page = request.GET.get('page')
    try:
        plans = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        plans = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        plans = paginator.page(paginator.num_pages)

    return render(request, "caseplan-detail.html", {"user": username,"test_plan":plans,"plan_id":plan_id,"test_type":test_type,'app':'APP','web':'WEB','api':'API'})

'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

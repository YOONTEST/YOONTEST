#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Testcase,Repository,Key_repository,Teststep,Teststep_api,Plan_case
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import os
import time
import urllib
import requests
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from api_v1 import test_data


logger = logging.getLogger(__name__)
#=========================CASE=================================================
# 用例管理
@login_required
def case(request,platform):
    if platform=="web" or platform=="api":
        case_list = Testcase.objects.filter(platform = platform).order_by("testcase_name")
    else:
        case_android = Testcase.objects.filter(platform = 'android').order_by("testcase_name")
        case_ios = Testcase.objects.filter(platform = 'ios').order_by("testcase_name")
        case_list = case_android | case_ios
    username = request.session.get('username','')
    if platform=='ios' or platform=="android":
        platform="app"
    paginator = Paginator(case_list,20)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)

    return render(request, "case.html", {"user": username,"platform":platform,"test_case":cases})

# 用例管理
@login_required
def add_case(request,platform):
    username = request.session.get('username', '')
    project = Key_repository.objects.filter(key_type='project')
    return render(request, "add_case.html", {"user": username,"project":project,"test_case":"","platform":platform})

@login_required
def add_case_action(request):
    username = request.session.get('username', '')
    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例集名
    project_name = request.POST.get('project_name','')         # 项目名
    project_id = ""                                            # 项目ID
    id = Key_repository.objects.filter(key_name=project_name)
    for x in id:
        project_id = x.key_value
    platform = request.POST.get('platform','')                  # 项目名
    environment = request.POST.get('environment','')            # 环境
    temp_platform=""
    if platform=="ios" or platform=="android":
        temp_platform="app"
    else:
        temp_platform=platform

    case = Testcase.objects.filter(scenario_name =scenario_name,testcase_name=testcase_name)
    if len(case):
        return HttpResponseRedirect('/case/'+temp_platform+'/')
    if scenario_name=="" or testcase_name=="":
        return HttpResponseRedirect('/case/'+temp_platform+'/')
    else:
        Testcase.objects.create(scenario_name=scenario_name,testcase_name=testcase_name,project_id=project_id,project_name=project_name,platform=platform,environment=environment)
    #case_list = Testcase.objects.all()
    #return render(request, 'case.html',{"user": username,"test_case":case_list})
    return HttpResponseRedirect('/case/'+temp_platform+'/')

# 用例管理
@login_required
def edit_case(request,testcase_id):
    case = Testcase.objects.filter(id=testcase_id)
    username = request.session.get('username', '')
    project = Key_repository.objects.filter(key_type='project')
    return render(request, "add_case.html", {"user": username,"project":project,"test_case":case})

@login_required
def view_case(request,testcase_id):
    case = Testcase.objects.filter(id=testcase_id)
    username = request.session.get('username', '')
    return render(request, "view_case.html", {"user": username,"test_case":case})

# 用例管理
@login_required
def edit_case_action(request):
    username = request.session.get('username', '')
    testcase_id = request.POST.get('testcase_id','')           # 用例集名
    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例名
    project_name = request.POST.get('project_name','')         # 项目名
    project_id = ""                                            # 项目ID
    id = Key_repository.objects.filter(key_name=project_name)
    for x in id:
        project_id = x.key_value
    platform = request.POST.get('platform','')                  # 项目名
    environment = request.POST.get('environment','')            # 环境
    temp_platform=""
    if platform=="ios" or platform=="android":
        temp_platform="app"
    else:
        temp_platform=platform
    case = Testcase.objects.filter(id=testcase_id)
    case.update(scenario_name=scenario_name,testcase_name=testcase_name,project_id=project_id,project_name=project_name)
    mapping_list = Plan_case.objects.filter(case_id=testcase_id)
    for mapping in mapping_list:
        one_mapping=Plan_case.objects.filter(plan_id=mapping.plan_id,case_id=mapping.case_id)
        try:
            one_mapping.update(id=mapping.id,plan_id=mapping.plan_id, case_id=mapping.case_id, scenario_name=scenario_name,testcase_name=testcase_name,platform=platform,environment=environment)
        except Exception as e:
            print(e)

    return HttpResponseRedirect('/case/'+temp_platform+'/')

# 用例管理
@login_required
def delete_case_action(request,testcase_id):
    username = request.session.get('username', '')
    test_case = get_object_or_404(Testcase, id=testcase_id)
    case = Testcase.objects.filter(id=testcase_id)
    platform=''
    for x in case:
        platform = x.platform
    case.delete()
    step = Teststep.objects.filter(case_id=testcase_id)
    step.delete()
    step = Teststep_api.objects.filter(case_id=testcase_id)
    step.delete()
    return HttpResponseRedirect('/case/'+platform+'/')

#=========================APP========================================================
@login_required
def step_app(request,case_id,step_id,action):
    username = request.session.get('username', '')
    repository = Repository.objects.exclude(platform='web')
    action_list = Key_repository.objects.filter(key_type='action')
    assert_list = Key_repository.objects.filter(key_type='assert')
    step_name_list=[]

    for i in range(99):
        str_1="step"
        if i+1 > 10:
            str_2="0"+str(i)
        else:
            str_2="00"+str(i)
        step_name_list.append(str_1+str_2)
    print(step_name_list)

    if action=='add':
            step_name = request.POST.get('step_name','')        # 用例集名
            how = request.POST.get('how','')                    # 用例集名
            which = request.POST.get('which','')                # 步骤名
            what = request.POST.get('what','')                  # 项目ID
            expected = request.POST.get('expected','')          # 项目名
            check_type = request.POST.get('check_type','')      # 项目名
            step_one=Teststep.objects.filter(id =step_id)
            if len(step_one):
                if step_name=="" or how=="":
                    return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')
                else:
                    step_one.update(case_id=case_id,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')

            else:
                step = Teststep.objects.filter(case_id =case_id,step_name=step_name)
                if len(step):
                    return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')
                if step_name=="" or how=="":
                    return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')
                else:
                    Teststep.objects.create(case_id=case_id,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')

    elif action=="delete":
            test_step = get_object_or_404(Teststep, id=step_id)
            step = Teststep.objects.filter(id=step_id)
            step.delete()
            return HttpResponseRedirect('/step_app/view/'+case_id+'/0/')

    elif action=='view':
            if step_id=="0":
                step_list = Teststep.objects.filter(case_id=case_id).order_by('step_name')
                return render(request, "step_app.html", {"user": username,"one_step":"","case_id":case_id,"repository":repository,"action_list":action_list,"assert_list":assert_list,"step_list":step_list,"case_id":case_id,"step_name_list":step_name_list})
            else:
                one_step = Teststep.objects.filter(case_id=case_id,id=step_id)
                step_list = Teststep.objects.filter(case_id=case_id).order_by('step_name')
                return render(request, "step_app.html", {"user": username,"one_step":one_step,"case_id":case_id,"repository":repository,"action_list":action_list,"assert_list":assert_list,"step_list":step_list,"case_id":case_id,"step_name_list":step_name_list})


#==========================WEB==============================================================
@login_required
def step_web(request,case_id,step_id,action):
    username = request.session.get('username', '')
    repository = Repository.objects.filter(platform='web')
    action_list = Key_repository.objects.filter(key_type='action')
    assert_list = Key_repository.objects.filter(key_type='assert')
    step_name_list=[]

    for i in range(99):
        str_1="step"
        if i+1 > 9:
            str_2="0"+str(i+1)
        else:
            str_2="00"+str(i+1)
        step_name_list.append(str_1+str_2)


    if action=='add':
            step_name = request.POST.get('step_name','')        # 用例集名
            how = request.POST.get('how','')                    # 用例集名
            which = request.POST.get('which','')                # 步骤名
            what = request.POST.get('what','')                  # 项目ID
            expected = request.POST.get('expected','')          # 项目名
            check_type = request.POST.get('check_type','')      # 项目名
            step_one=Teststep.objects.filter(id =step_id)

            if len(step_one):
                if step_name=="" or how=="":
                    return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')
                else:
                    step_one.update(case_id=case_id,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')

            else:
                step = Teststep.objects.filter(case_id =case_id,step_name=step_name)
                if len(step):
                    return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')
                if step_name=="" or how=="":
                    return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')
                else:
                    Teststep.objects.create(case_id=case_id,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')

    elif action=="delete":
            test_step = get_object_or_404(Teststep, id=step_id)
            step = Teststep.objects.filter(id=step_id)
            step.delete()
            return HttpResponseRedirect('/step_web/view/'+case_id+'/0/')

    elif action=='view':
            if step_id=="0":
                step_list = Teststep.objects.filter(case_id=case_id).order_by('step_name')
                return render(request, "step_web.html", {"user": username,"one_step":"","case_id":case_id,"repository":repository,"action_list":action_list,"assert_list":assert_list,"step_list":step_list,"case_id":case_id,"step_name_list":step_name_list})
            else:
                one_step = Teststep.objects.filter(case_id=case_id,id=step_id)
                step_list = Teststep.objects.filter(case_id=case_id).order_by('step_name')
                return render(request, "step_web.html", {"user": username,"one_step":one_step,"case_id":case_id,"repository":repository,"action_list":action_list,"assert_list":assert_list,"step_list":step_list,"case_id":case_id,"step_name_list":step_name_list})


#=====================================API===================================
# 用例管理
@login_required
def run_api_script(request,case_id):
    username = request.session.get('username', '')
    scenario_name = testcase_name = ""
    one_case = Testcase.objects.filter(id = case_id)
    for one in one_case:
        scenario_name = one.scenario_name
        testcase_name = one.testcase_name
    test_case = test_data.api_test_case(scenario_name,testcase_name)[0]
    test_how = test_case.get("how")
    test_which = test_case.get("which")
    test_headers = test_case.get('headers')
    test_body = test_case.get('body')

    result={}

    try:
        if test_how=="get":
            response=requests.get(test_which,headers=test_headers,verify=False)
            result = str(response.json())
            result = result.replace(u'\u2022',u'·')
            result = eval(result)
            #print(result)
        if test_how=="post":
            response=requests.post(test_which,headers=test_headers,json=test_body,verify=False)
            result = str(response.json())
            result = result.replace(u'\u2022',u'·')
            result = eval(result)
            #print(result)
        if test_how=="put":
            response=requests.put(test_which,headers=test_headers,json=test_body,verify=False)
            result = str(response.json())
            result = result.replace(u'\u2022',u'·')
            result = eval(result)
            #print(result)
        if test_how=="delete":
            response=requests.delete(test_which,headers=test_headers,json=test_body,verify=False)
            result = str(response.json())
            result = result.replace(u'\u2022',u'·')
            result = eval(result)
            #print(result)
    except requests.exceptions.ConnectionError as e:
        print(e)

    return render(request, "run_api_script.html", {"user": username,"result":result})

# 用例管理
def step_api(request,case_id,step_id,action):
    username = request.session.get('username', '')
    repository = Repository.objects.filter(platform='api')
    http_method = Key_repository.objects.filter(key_type='method')
    assert_list = Key_repository.objects.filter(key_type='assert')
    step_name_list=[]

    for i in range(99):
        str_1="step"
        if i+1 > 9:
            str_2="0"+str(i+1)
        else:
            str_2="00"+str(i+1)
        step_name_list.append(str_1+str_2)


    if action=='add':
            how = request.POST.get('how','')                    # 方法
            which = request.POST.get('which','')                # URL
            headers = request.POST.get('headers','')            # 头部信息
            body = request.POST.get('body','')                  # 内容信息
            parameters = request.POST.get('parameters','')      # 参数
            expected = request.POST.get('expected','')          # 期望
            check_type = request.POST.get('check_type','')      # 断言类型

            step_one = Teststep_api.objects.filter(case_id = case_id)

            if len(step_one):
                step_one.update(case_id=case_id,how=how,which=which,headers=headers,body=body,parameters=parameters,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/case/api/')
            else:
                Teststep_api.objects.create(case_id=case_id,how=how,which=which,headers=headers,body=body,parameters=parameters,expected=expected,check_type=check_type)
                return HttpResponseRedirect('/case/api/')

    elif action=='view':
            one_step = Teststep_api.objects.filter(case_id=case_id)
            if len(one_step):
                return render(request, "step_api.html", {"user": username,"one_step":one_step,"case_id":case_id,"http_method":http_method,"assert_list":assert_list})
            else:
                return render(request, "step_api.html", {"user": username,"one_step":"","case_id":case_id,"http_method":http_method,"assert_list":assert_list})



'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

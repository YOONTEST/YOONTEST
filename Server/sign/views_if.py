#coding=utf-8
from django.http import JsonResponse
from sign.models import Testcase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import generics
from sign.serializers import UserSerializer, GroupSerializer,TestcaseSerializer
from rest_framework import permissions, viewsets, renderers
from rest_framework.decorators import (
    permission_classes, detail_route
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render
from django.http import JsonResponse
import time

# 添加测试用例接口
def add_testcase(request):
    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例名
    step_name = request.POST.get('step_name','')               # 步骤名
    how = request.POST.get('how','')                           # 方法
    which = request.POST.get('which','')                       # URL
    what = request.POST.get('what','')                         # 参数
    expected = request.POST.get('expected','')                     # 期望结果
    check_type= request.POST.get('check_type','')              # 检查类型
    status_code = request.POST.get('status_code','')           # 状态码
    run_times = request.POST.get('run_times','')                 # 执行次数
    auth_user = request.POST.get('auth_user','')               # 用户
    auth_password = request.POST.get('auth_password','')       # 密码
    project_id = request.POST.get('project_id','')             # 项目ID
    project_name = request.POST.get('project_name','')         # 项目名

    if scenario_name =='' or testcase_name =='' or step_name =='' or check_type =='' or run_times =='' or status_code =='' or project_id =='' or project_name =='' or how =='' or which =='' or expect =='':
        return JsonResponse({'status':10021,'message':'缺失参数'})

    result = Testcase_api.objects.filter(scenario_name=scenario_name,testcase_name=testcase_name)
    if result:
        return JsonResponse({'status':10022,'message':'测试用例存在'})

    try:
        Testcase_api.objects.create(scenario_name=scenario_name,testcase_name=testcase_name,step_name=step_name,how=how,which=which,expect=expect,check_type=check_type,status_code=status_code,run_times=run_times,auth_user=auth_user,auth_password=auth_password,project_id=project_id,project_name=project_name)
        return JsonResponse({'status':200,'message':'成功添加测试用例'})
    except Exception as e:
        return JsonResponse({'status':10024,'message':'添加测试用例失败'})

# 测试用例查询
def get_testcase(request):

    scenario_name = request.GET.get("scenario_name", "")        # 测试集
    testcase_name = request.GET.get("testcase_name", "")
    project_name = request.GET.get("project_name", "")         # 测试用例

    #if scenario_name == '':
    #    return JsonResponse({'status':10021,'message':'缺失参数'})

    if scenario_name != '' and testcase_name != '':
        testcase = {}
        try:
            result = Testcase.objects.get(scenario_name=scenario_name,testcase_name=testcase_name)
            #return JsonResponse({'status':10022, 'message':result})
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            testcase['id'] = result.id
            testcase['scenario_name'] = result.scenario_name
            testcase['testcase_name'] = result.testcase_name
            testcase['step_name'] = result.step_name
            testcase['how'] = result.how
            testcase['which'] = result.which
            testcase['what'] = result.what
            testcase['expected'] = result.expected
            testcase['check_type'] = result.check_type
            testcase['run_times'] = result.run_times
            testcase['status_code'] = result.status_code
            testcase['auth_user'] = result.auth_user
            testcase['auth_password'] = result.auth_password
            testcase['project_id'] = result.project_id
            testcase['project_name'] = result.project_name
            testcase['create_time'] = result.create_time
            return JsonResponse({'status':200, 'message':'success', 'data':testcase})

    if scenario_name != '':
        datas = []
        results = Testcase.objects.filter(scenario_name__contains=scenario_name)
        if results:
            for r in results:
                testcase = {}
                testcase['id'] = r.id
                testcase['scenario_name'] = r.scenario_name
                testcase['testcase_name'] = r.testcase_name
                testcase['step_name'] = r.step_name
                testcase['how'] = r.how
                testcase['which'] = r.which
                testcase['what'] = r.what
                testcase['expected'] = r.expected
                testcase['check_type'] = r.check_type
                testcase['run_times'] = r.run_times
                testcase['status_code'] = r.status_code
                testcase['auth_user'] = r.auth_user
                testcase['auth_password'] = r.auth_password
                testcase['project_id'] = r.project_id
                testcase['project_name'] = r.project_name
                testcase['create_time'] = r.create_time
                datas.append(testcase)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

    if project_name != '':
        datas = []
        results = Testcase.objects.filter(project_name__contains=project_name)
        if results:
            for r in results:
                testcase = {}
                testcase['id'] = r.id
                testcase['scenario_name'] = r.scenario_name
                testcase['testcase_name'] = r.testcase_name
                testcase['step_name'] = r.step_name
                testcase['how'] = r.how
                testcase['which'] = r.which
                testcase['what'] = r.what
                testcase['expected'] = r.expected
                testcase['check_type'] = r.check_type
                testcase['run_times'] = r.run_times
                testcase['status_code'] = r.status_code
                testcase['auth_user'] = r.auth_user
                testcase['auth_password'] = r.auth_password
                testcase['project_id'] = r.project_id
                testcase['project_name'] = r.project_name
                testcase['create_time'] = r.create_time
                datas.append(testcase)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
    return JsonResponse({'status':200, 'message':'success','data':{}})

class TestcaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows test_case to be viewed or edited.
    """
    queryset = Testcase.objects.all()
    serializer_class = TestcaseSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('scenario_name', 'testcase_name')

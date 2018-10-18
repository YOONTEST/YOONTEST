#coding=utf-8
# author:kang
# 加载API测试数据接口
from django.http import JsonResponse
import time
import datetime
import urllib
from sign.models import Key_repository
from sign.models import Device
from sign.models import Testcase
from sign.models import Teststep
from sign.models import Teststep_api
from sign.models import Repository
from sign.models import Test_plan
from sign.models import Plan_case
from sign.models import Activity
from sign.models import Slaves
from sign.models import Slaves_logs
from sign.models import Execution
from sign.models import Run_time_data
from api_v1 import custom_data
#from django.core import serializers

def slave(request): #启动/关闭分支接口
    slave_name = request.GET.get('slave','')  #分支机器名
    status = request.GET.get('status','')     #分支机器状态
    
    print(slave_name)
    one_slave = Slaves.objects.filter(slave_name=slave_name)
    now_time = datetime
    if status=="up":
        if len(one_slave):
            pass
        else:
            Slaves.objects.create(slave_name =slave_name)
            Slaves_logs.objects.create(slave_name = slave_name,status="up",create_time=str(now_time))
    elif status =="down":
        if len(one_slave):
            one_slave.delete()
            Slaves_logs.objects.create(slave_name = slave_name,status="down",create_time=str(now_time))
    else:
        pass
    return JsonResponse({'data':"success"})
    

def get_activity(request):#获取执行活动接口
    slave_name = request.GET.get('slave','')  #分支机器名
    one_activity = Activity.objects.filter(slave_name=slave_name)
    plan_name = activity_id = test_type = device = ""
    for one in one_activity:
        print(one.status)
        if one.status == "pending":
            plan_name = one.plan_name
            activity_id = one.id
            test_type = one.test_type
            device = one.device_name
    data = {"plan_name":plan_name,"activity_id":activity_id,"test_type":test_type,"device":device}
       
    return JsonResponse({'data': data})

def get_device(request):#获取执行活动接口
    device_name = request.GET.get('device','')  #分支机器名
    one_device = Device.objects.filter(name=device_name)
    device_info = ""
    for one in one_device:
        device_info = one.device_info
    data = {"device_info":device_info}
       
    return JsonResponse({'data': data})


def set_activity(request):#设置执行活动状态
    activity_id = request.GET.get('activity_id','')  #活动ID
    status = request.GET.get('status','')            #活动状态
    one_activity = Activity.objects.filter(id=activity_id)
    one_activity.update(status=status)
    return JsonResponse({'data':"success"})


def get_run_list(request):#获取测试计划中测试用例列表
    plan_name = request.GET.get('plan_name','')
    one_plan = Test_plan.objects.filter(plan_name=plan_name)
    test_type = plan_id = ""
    
    for one in one_plan:
        plan_id = one.id 
        test_type = one.test_type 
    data = []
    one_plan_case = Plan_case.objects.filter(plan_id=plan_id).order_by("scenario_name","testcase_name")
    for one in one_plan_case:
        one_case = {}
        scenario_name = one.scenario_name
        testcase_name = one.testcase_name
        one_case = {"testcase_name":testcase_name,"scenario_name":scenario_name}
        data.append(one_case)

    return JsonResponse({'data': data})

def get_test_case(request):#获取测试用例内容
    scenario_name = request.GET.get('scenario_name','')
    testcase_name = request.GET.get('testcase_name','')
    test_type = request.GET.get('test_type','')
    data = []
    if test_type=="api":
        data = api_test_case(scenario_name,testcase_name)
    elif test_type == "web" or test_type=="app":
        data = test_case(scenario_name,testcase_name)
        
    return JsonResponse({'data': data})

#====================================API===========================================================================
def api_test_case(scenario_name,testcase_name): #获取接口测试用例
    case_id = project_id = environment = environment_url = ""
    one_test_case =  Testcase.objects.filter(scenario_name=scenario_name,testcase_name=testcase_name)
    for case in one_test_case:
        case_id = case.id
        project_id = case.project_id
        environment = case.environment
    key_name = environment+"_"+project_id
    environments = Key_repository.objects.filter(key_type='environment',key_name=key_name)
    
    for one in environments:
        environment_url = one.key_value
    
    steps = Teststep_api.objects.filter(case_id = case_id)
    data = []

    for step in steps:
        temp_which = environment_url+step.which
        temp_headers = step.headers
        temp_body = step.body
        temp_parameters = step.parameters
        
        new_step = api_format_data(temp_which,temp_headers,temp_body,temp_parameters)
        which = new_step.get("which")
        headers = new_step.get("headers")
        if headers=="None":
            headers=""
        body = new_step.get("body")
        if body=="None":
            body=""
        parameters = new_step.get("parameters")
        how = step.how
        check_type = step.check_type
        expected = step.expected
        if expected=="None":
            expected=""
        
        data.append({"how":how,"which":which,"headers":headers,"body":body,"expected":expected,"parameters":parameters,"check_type":check_type})
    return data

def api_format_data(which,headers,body,parameters): #格式化接口测试数据
        #返回格式化后的测试数据
        new_step={}
        str_which = str(which)
        if parameters:
            dict_parameters = eval(parameters)
            str_headers = str(headers)
            str_body = str(body)

            for key in dict_parameters:
                current_key = str(dict_parameters[key])
                current_key = current_key.replace(' ','')
                if "{{" in current_key:
                    cmd = current_key[2:-2]
                    dict_parameters[key]=eval("custom_data.getdata()."+cmd)
                    #print(dict_parameters[key])

            for key in dict_parameters: #根据商户会员手机号获取商户ID
                current_value = str(dict_parameters.get(key))
                if "${"+key+"}" in str_body:
                    str_body=str_body.replace("${"+key+"}",current_value)
                if "${"+key+"}" in str_which:
                    str_which=str_which.replace("${"+key+"}",current_value)
                if "${"+key+"}" in str_headers:
                    str_headers=str_headers.replace("${"+key+"}",current_value)
        else:
            str_headers={}
            str_body={}

        if which.strip():
            new_step["which"]=str_which

        if headers.strip():
            if isinstance(headers,str):
                new_step["headers"]=eval(str_headers)
        else:
            new_step["headers"]={}

        if body.strip():
            if isinstance(body,str):
                new_step["body"]=eval(str_body)
        else:
            new_step["body"]={}
        return new_step
#=================================WEB and APP=========================================================
def test_case(scenario_name,testcase_name): #获取WEB，APP测试用例
    case_id = ""
    one_test_case =  Testcase.objects.filter(scenario_name=scenario_name,testcase_name=testcase_name)
    for case in one_test_case:
        case_id = case.id
        
    steps = Teststep.objects.filter(case_id = case_id).order_by("step_name")
    data = []

    for step in steps:
        how = which = what = find_by = find_by_value = check_type = ""     
        step_name = step.step_name
        one_how = Key_repository.objects.filter(key_type="action",key_name=step.how)
        for one in one_how:
            how = one.key_value

        one_check_type = Key_repository.objects.filter(key_type="assert",key_name=step.check_type)
        for one in one_check_type:
            check_type = one.key_value
        
        expected = step.expected
        
        one_element = Repository.objects.filter(key=step.which)
        for one in one_element:
            find_by = one.find_by
            find_by_value = one.find_by_value
        what = step.what
        which = {find_by:find_by_value}
        new_data = format_which(which,what)
        
        what = new_data.get("what")
        which = new_data.get("which")
    
        data.append({"step_name":step_name,"how":how,"which":which,"what":what,"check_type":check_type,"expected":expected})
    return data
    
def format_which(which,what): #格式化 WHICH 数据
    temp_which=which
    temp_what=what
    if temp_what:
        if "{{" in temp_what and "}}" in temp_what:
            s_index = temp_what.find("{{")+2
            e_index = temp_what.find("}}")
            
            cmd = temp_what[s_index:e_index]
            result = eval("custom_data.getdata()."+cmd)
            temp_what= temp_what.replace("{{"+cmd+"}}",result)

        if "{from_what}" in str(which):
            temp_which = str(which).replace("{from_what}",temp_what)
            temp_which=eval(temp_which)
    
    if temp_which:
        if "{{" in temp_which and "}}" in temp_which:
            s_index = temp_which.find("{{")+2
            e_index = temp_which.find("}}")
            
            cmd = temp_which[s_index:e_index]
            result = eval("custom_data.getdata()."+cmd)
            temp_which= temp_which.replace("{{"+cmd+"}}",result)
        
    return {"which":temp_which,"what":temp_what}

    
def upload_results(request):#上传测试结果
    data = request.GET.get('data','')
    data=urllib.request.unquote(data) 
    data = eval(data)
    if isinstance(data,dict):
        suitename = data.get('scenario_name')
        casename = data.get('testcase_name')
        casestatus = data.get('tc_result')
        errorcontent = data.get('tc_result_msg')
        starttime = data.get('start_time')
        endtime = data.get('end_time')
        caseRunningtime = data.get('response_time')
        how = data.get('how')
        which = data.get('which')
        headers = data.get('headers')
        body = data.get('body')
        request_data = {"METHOD":how,"URL":which,"HEADERS":headers,"BODY":body}
        response_results = data.get('response_results')
        activity_id = data.get('activity_id')
        apptype = data.get('test_type')
        report_summaryid=str(int(time.time()))
        Execution.objects.create(suitename=suitename,casename=casename,casestatus=casestatus,errorcontent=errorcontent,starttime=starttime,endtime=endtime,caseRunningtime=caseRunningtime,request_data=request_data,response_results=response_results,apptype=apptype,activity_id=activity_id,report_summaryid=report_summaryid)
    return JsonResponse({'message':"success"})

# 上传run-time数据
def upload_run_time(request):
    activity_id = request.GET.get('activity_id','')
    activity_id=urllib.request.unquote(activity_id)
    plan_id = request.GET.get('plan_id','')
    plan_id=urllib.request.unquote(plan_id)
    case_id = request.GET.get('case_id','')
    case_id=urllib.request.unquote(case_id)
    key = request.GET.get('key','')
    key=urllib.request.unquote(key)
    value = request.GET.get('value','')
    value=urllib.request.unquote(value)

    Run_time_data.objects.create(activity_id=activity_id,plan_id=plan_id,case_id=case_id,key=key,value=value)
    return JsonResponse({'message':"success"})

def get_run_time(request):
    activity_id = request.GET.get('activity_id','')
    activity_id=urllib.request.unquote(activity_id)
    key = request.GET.get('key','')
    key=urllib.request.unquote(key)

    run_data = Run_time_data.objects.filter(activity_id=activity_id,key=key)
    value = ""
    for one in run_data:
        value = one.value

    return JsonResponse({key:value})
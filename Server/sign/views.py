#coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Reportlist
from sign.models import Execution
from sign.models import Device
from sign.models import Testcase
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

# Create your views here.
# 首页(登录)
def index(request):
    return render(request,"index.html")

# 登录动作
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == '' or password == '':
            return render(request,"index.html",{"error":"username or password null!"})
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/home/') # 登录成功跳转发布会管理
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
        else:
            return render(request,"index.html",{"error":"username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request,"index.html")

# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 首页（登录之后默认页面）
@login_required
def home(request):
    case_list = Testcase.objects.all()
    api_list = Testcase.objects.filter(platform='api')
    app_android = Testcase.objects.filter(platform='android')
    app_ios = Testcase.objects.filter(platform='ios')
    app_list = app_android|app_ios
    web_list = Testcase.objects.filter(platform='web')

    total_number = str(len(case_list ))
    api_number = str(len(api_list))
    app_number = str(len(app_list))
    web_number=str(len(web_list))

    username = request.session.get('username', '')
    return render(request, "home.html", {"user": username,"api":api_number,"app":app_number,"web":web_number,"all":total_number})


# 用例管理
@login_required
def case_api(request):
    case_list = Testcase_api.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)

    return render(request, "case-api.html", {"user": username,"test_case":cases})

@login_required
def case_app(request):
    case_list = Testcase_api.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)

    return render(request, "case-app.html", {"user": username,"test_case":cases})
#设备名称列表
@login_required
def devices(request):
    case_list = Device.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)

    return render(request, "device.html", {"user": username,"test_case":cases})

#ui对象管理
@login_required
def repositorys(request):
    case_list = repository.objects.all()
    username = request.session.get('username', '')
    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)

    return render(request, "repository.html", {"user": username,"test_case":cases})

#report测试报告下载方法
@login_required
def report_download(request,project_name):
    project_name=urllib.request.unquote(project_name)
    with open("..\\Result\\api\\report\\"+project_name+".html") as f:
        c = f.read()
    return HttpResponse(c)

# 报告管理
@login_required
def report(request,project_name):
    if project_name!="all":
        report_list = reportlist.objects.filter(apptype=project_name).order_by('-Creation_time')
    else:
        report_list = reportlist.objects.all().order_by('-Creation_time')
    username = request.session.get('username', '')

    vinci = reportlist.objects.filter(apptype="vinci")
    life = reportlist.objects.filter(apptype="life")
    business = reportlist.objects.filter(apptype="business")
    report = reportlist.objects.all()
    vinci_number=str(len(vinci))
    life_number=str(len(life))
    business_number=str(len(business))
    all_number=str(len(report))
    return render(request, "report.html", {"user": username,"report_list":report_list,"vinci_number":vinci_number,"life_number":life_number,"business_number":business_number,"all_number":all_number})

# 用例管理
@login_required
def add_case_api(request):
    username = request.session.get('username', '')
    return render(request, "add_case_api.html", {"user": username,"test_case":""})

@login_required
def add_case_app(request):
    username = request.session.get('username', '')
    return render(request, "add_case_app.html", {"user": username,"test_case":""})
@login_required
def add_case_api_action(request):
    username = request.session.get('username', '')

    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例集名
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


    case = Testcase_api.objects.filter(scenario_name =scenario_name,testcase_name=testcase_name)
    if len(case):
        return HttpResponseRedirect('/case/')
    if scenario_name=="" or testcase_name=="":
        return HttpResponseRedirect('/case/')
    else:
        Testcase_api.objects.create(scenario_name=scenario_name,testcase_name=testcase_name,step_name=step_name,how=how,which=which,expected=expected,check_type=check_type,status_code=status_code,run_times=run_times,auth_user=auth_user,auth_password=auth_password,project_id=project_id,project_name=project_name)
    #case_list = Testcase_api.objects.all()
    #return render(request, 'case.html',{"user": username,"test_case":case_list})
    return HttpResponseRedirect('/case-api/')

@login_required
def add_case_app_action(request):
    username = request.session.get('username', '')

    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例集名
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


    case = Testcase_api.objects.filter(scenario_name =scenario_name,testcase_name=testcase_name)
    if len(case):
        return HttpResponseRedirect('/case/')
    if scenario_name=="" or testcase_name=="":
        return HttpResponseRedirect('/case/')
    else:
        Testcase_api.objects.create(scenario_name=scenario_name,testcase_name=testcase_name,step_name=step_name,how=how,which=which,expected=expected,check_type=check_type,status_code=status_code,run_times=run_times,auth_user=auth_user,auth_password=auth_password,project_id=project_id,project_name=project_name)
    #case_list = Testcase_api.objects.all()
    #return render(request, 'case.html',{"user": username,"test_case":case_list})
    return HttpResponseRedirect('/case-app/')



# 用例管理
@login_required
def edit_case_api(request,testcase_id):
    case = Testcase_api.objects.filter(id=testcase_id)
    #case_data = str(len(case))
    username = request.session.get('username', '')
    return render(request, "add_case_api.html", {"user": username,"test_case":case})

@login_required
def view_case_api(request,testcase_id):
    case = Testcase_api.objects.filter(id=testcase_id)
    #case_data = str(len(case))
    username = request.session.get('username', '')
    return render(request, "view_case_api.html", {"user": username,"test_case":case})

@login_required
def edit_case_app(request,testcase_id):
    case = Testcase_api.objects.filter(id=testcase_id)
    #case_data = str(len(case))
    username = request.session.get('username', '')
    return render(request, "add_case_app.html", {"user": username,"test_case":case})


# 用例管理
@login_required
def edit_case_api_action(request):
    username = request.session.get('username', '')
    #test_case = get_object_or_404(Testcase, id=testcase_id)
    #case = Testcase_api.objects.filter(id=testcase_id)
    testcase_id = request.POST.get('testcase_id','')       # 用例集名
    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例名
    step_name = request.POST.get('step_name','')               # 步骤名
    how = request.POST.get('how','')                           # 方法
    which = request.POST.get('which','')                       # URL
    what = request.POST.get('what','')                         # 参数
    expected = request.POST.get('expected','')                 # 期望结果
    check_type= request.POST.get('check_type','')              # 检查类型
    status_code = request.POST.get('status_code','')           # 状态码
    run_times = request.POST.get('run_times','')                 # 执行次数
    auth_user = request.POST.get('auth_user','')               # 用户
    auth_password = request.POST.get('auth_password','')       # 密码
    project_id = request.POST.get('project_id','')             # 项目ID
    project_name = request.POST.get('project_name','')         # 项目名

    case = Testcase_api.objects.filter(id=testcase_id)
    case.update(scenario_name=scenario_name,testcase_name=testcase_name,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type,status_code=status_code,run_times=run_times,auth_user=auth_user,auth_password=auth_password,project_id=project_id,project_name=project_name)

    case_list = Testcase_api.objects.all()
    #return render(request, 'case.html',{"user": username,"test_case":case_list})
    return HttpResponseRedirect('/case-api/')

@login_required
def edit_case_app_action(request):
    username = request.session.get('username', '')
    #test_case = get_object_or_404(Testcase, id=testcase_id)
    #case = Testcase_api.objects.filter(id=testcase_id)
    testcase_id = request.POST.get('testcase_id','')       # 用例集名
    scenario_name = request.POST.get('scenario_name','')       # 用例集名
    testcase_name = request.POST.get('testcase_name','')       # 用例名
    step_name = request.POST.get('step_name','')               # 步骤名
    how = request.POST.get('how','')                           # 方法
    which = request.POST.get('which','')                       # URL
    what = request.POST.get('what','')                         # 参数
    expected = request.POST.get('expected','')                 # 期望结果
    check_type= request.POST.get('check_type','')              # 检查类型
    status_code = request.POST.get('status_code','')           # 状态码
    run_times = request.POST.get('run_times','')                 # 执行次数
    auth_user = request.POST.get('auth_user','')               # 用户
    auth_password = request.POST.get('auth_password','')       # 密码
    project_id = request.POST.get('project_id','')             # 项目ID
    project_name = request.POST.get('project_name','')         # 项目名

    case = Testcase_api.objects.filter(id=testcase_id)
    case.update(scenario_name=scenario_name,testcase_name=testcase_name,step_name=step_name,how=how,which=which,what=what,expected=expected,check_type=check_type,status_code=status_code,run_times=run_times,auth_user=auth_user,auth_password=auth_password,project_id=project_id,project_name=project_name)

    case_list = Testcase_api.objects.all()
    #return render(request, 'case.html',{"user": username,"test_case":case_list})
    return HttpResponseRedirect('/case-app/')

# 用例管理
@login_required
def delete_case_api_action(request,testcase_id):
    username = request.session.get('username', '')
    test_case = get_object_or_404(Testcase_api, id=testcase_id)
    case = Testcase_api.objects.filter(id=testcase_id)
    case.delete()
    case_list = Testcase_api.objects.all()
    return HttpResponseRedirect('/case-api/')

@login_required
def delete_case_app_action(request,testcase_id):
    username = request.session.get('username', '')
    test_case = get_object_or_404(Testcase_api, id=testcase_id)
    case = Testcase_api.objects.filter(id=testcase_id)
    case.delete()
    case_list = Testcase_api.objects.all()
    return HttpResponseRedirect('/case-app/')

# 用例名称搜索
@login_required
def search_contents_api(request):
    username = request.session.get('username', '')
    search_contents = request.GET.get("contents", "")
    search_contents_bytes = search_contents.encode(encoding="utf-8")

    case_list = Testcase_api.objects.filter(testcase_name__contains=search_contents_bytes)

    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)


    return render(request, "case-api.html", {"user": username, "test_case": cases})

@login_required
def search_contents_app(request):
    username = request.session.get('username', '')
    search_contents = request.GET.get("contents", "")
    search_contents_bytes = search_contents.encode(encoding="utf-8")

    case_list = Testcase_api.objects.filter(testcase_name__contains=search_contents_bytes)
    paginator = Paginator(case_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = paginator.page(paginator.num_pages)
    return render(request, "case-app.html", {"user": username, "test_case": cases})

# 执行脚本
@login_required
def execution(request):
    logs=[]
    log_folder='../Result/api/logs/'
    log_file=time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.log'
    if os.path.exists(log_folder+log_file):
        log_contents = open(log_folder+log_file, 'r')
        for line in log_contents:
            line = urllib.request.unquote(str(line))
            logs.append(line)
        if logs=="":
            logs = "暂无日志..."
    else:
        logs = "暂无日志..."

    username = request.session.get('username', '')

    #os.system("python D:\qianbao\Test_Terminator\Client\APIrunner_Jenkins.py")
    return render(request, "execution.html", {"user": username, "logs": logs})

@login_required
def download_logs(request):
    log_folder='../Result/api/logs/'
    log_file=time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.log'
    with open(log_folder+log_file) as f:
        c = f.read()
        c=urllib.request.unquote(c)
    return HttpResponse(c)

@login_required
def run_scripts(request):
    username = request.session.get('username', '')
    project_name = request.GET.get("project_name", "")
    if project_name!="all":
        os.system("python ..\Client\APIrunner_Jenkins.py "+project_name)
    else:
        os.system("python ..\Client\APIrunner_Jenkins.py")

    return HttpResponseRedirect('/execution/')

@login_required
def qr_code(request):
    username = request.session.get('username', '')
    return render(request, "qr-code.html", {"user": username})

@login_required
def links(request):
    username = request.session.get('username', '')
    return render(request, "links.html", {"user": username})

@login_required
def case(request):
    username = request.session.get('username', '')
    return render(request, "case.html", {"user": username})

# 用例管理
@login_required
def test_plan(request):
    plan_list = Test_plan.objects.all()
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

    return render(request, "test_plan.html", {"user": username,"test_plan":plans})
'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''

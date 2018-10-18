from django.db import models

#测试脚本
class Reportlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    report_name=models.CharField(max_length=100)            # 报告名
    Creation_time=models.DateTimeField()                    # 创建时间
    apptype=models.CharField(max_length=100)                # 项目名

    def __str__(self):
        return self.report_name

class Execution(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    casename=models.CharField(max_length=100)               # 用例名
    suitename=models.CharField(max_length=100)              # 用例集名
    casestatus=models.CharField(max_length=100)             # 用例状态
    errorcontent=models.TextField(max_length=10000)         # error内容
    report_summaryid=models.CharField(max_length=100)       # 报告ID
    caseRunningtime=models.CharField(max_length=100)        # Duration
    starttime=models.CharField(max_length=100)              # 开始时间
    endtime=models.CharField(max_length=100)                # 结束时间
    apptype=models.CharField(max_length=100)                # 项目名
    request_data=models.TextField(max_length=10000)         # 请求信息
    response_results=models.TextField(max_length=20000)     # 返回信息
    activity_id=models.CharField(max_length=100)            # 活动ID

    def __str__(self):
        return self.casename

class Device(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name=models.CharField(max_length=100)                   # 设备名
    app_name=models.CharField(max_length=100)               # 应用名
    device_info=models.CharField(max_length=1000)           # 设备应用信息

    def __str__(self):
        return self.deviceName

class Repository(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    key=models.CharField(max_length=100)                     # 关键字
    app=models.CharField(max_length=100)                     # 应用
    platform=models.CharField(max_length=45)                 # 平台
    find_by=models.CharField(max_length=100)                 # 查找方式
    find_by_value=models.CharField(max_length=2000)          # 查找参数

    def __str__(self):
        return self.key

class Test_plan(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    plan_name=models.CharField(max_length=111)                # 计划名
    test_type=models.CharField(max_length=45)                 # 测试类型

    def __str__(self):
        return self.plan_name

class Plan_case(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    case_id=models.CharField(max_length=100)                    # 用例ID
    scenario_name=models.CharField(max_length=100)              # 用例集名
    plan_id=models.CharField(max_length=100)                    # 计划ID
    testcase_name=models.CharField(max_length=100)              # 用例名

    class Meta:
        unique_together = ('plan_id', 'case_id')

    def __str__(self):
        return self.case_id,self.plan_id

class Testcase(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    scenario_name= models.CharField(max_length=100)            # 用例集名
    testcase_name = models.CharField(max_length=100)           # 用例名
    project_id = models.CharField(max_length=45)               # 项目ID
    project_name = models.CharField(max_length=45)             # 项目名
    create_time = models.DateTimeField(auto_now=True)          # 创建时间（自动获取当前时间）
    platform =  models.CharField(max_length=45)                # 项目ID
    environment =  models.CharField(max_length=45)             # 环境
    class Meta:
        unique_together = ('scenario_name', 'testcase_name')

    def __str__(self):
        return self.scenario_name,self.testcase_name

class Teststep(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    case_id= models.CharField(max_length=100)                   # 用例ID
    step_name = models.CharField(max_length=100)                # 步骤名
    how = models.CharField(max_length=100)                      # Action
    which = models.CharField(max_length=100)                    # 对象
    what = models.CharField(max_length=1000)                    # 参数
    expected = models.CharField(max_length=1000)                # 期望
    check_type = models.CharField(max_length=45)                # 断言类型
    create_time = models.DateTimeField(auto_now=True)          # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ('case_id', 'step_name')

    def __str__(self):
        return self.case_id,self.step_name

class Teststep_api(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    case_id= models.CharField(max_length=100)                  # 用例ID
    how = models.CharField(max_length=50)                      # 方法
    which = models.TextField(max_length=10000)                 # URL
    expected = models.TextField(max_length=10000)              # 期望结果
    check_type = models.CharField(max_length=50)               # 断言类型
    create_time = models.DateTimeField(auto_now=True)          # 创建时间（自动获取当前时间）
    headers = models.CharField(max_length=200)                 # 头部信息
    body = models.TextField(max_length=10000)                  # 内容
    parameters = models.TextField(max_length=10000)            # 参数

    def __str__(self):
        return self.case_id

class Key_repository(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    key_name= models.CharField(max_length=100)                  # 关键字
    key_value = models.CharField(max_length=100)                # 值
    key_type = models.CharField(max_length=100)                 # 类别

    class Meta:
        unique_together = ('key_name', 'key_value')

    def __str__(self):
        return self.key_name,self.key_value

class Slaves_logs(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    slave_name= models.CharField(max_length=100)                # 机器名
    status = models.CharField(max_length=100)                   # 机器状态
    create_time = models.DateTimeField(auto_now=True)           # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.slave_name

class Slaves(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    slave_name= models.CharField(max_length=100)                # 机器名

    def __str__(self):
        return self.slave_name

class Activity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    plan_name= models.CharField(max_length=100)                 # 计划名
    test_type= models.CharField(max_length=100)                 # 测试类型
    slave_name= models.CharField(max_length=100)                # 机器名
    device_name= models.CharField(max_length=100)               # 设备名
    status = models.CharField(max_length=100)                   # 活动状态
    create_time = models.DateTimeField(auto_now=True)           # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.slave_name,self.status


class Run_time_data(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    plan_id= models.CharField(max_length=100)                   # 计划ID
    activity_id= models.CharField(max_length=100)               # 活动ID
    case_id= models.CharField(max_length=100)                   # 用例ID
    key = models.CharField(max_length=100)                      # 关键字
    value = models.TextField(max_length=10000)                  # 值

    def __str__(self):
        return self.key

class Report_summary(models.Model):
    report_summaryid= models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='report_summaryid')
    Starttime= models.CharField(max_length=255)                 # 用例集名
    Endtime= models.CharField(max_length=255)                   # 用例集名
    Runningtime= models.CharField(max_length=255)               # 用例集名
    failures= models.CharField(max_length=255)                  # 用例集名
    Run= models.CharField(max_length=255)                       # 用例集名
    errors= models.CharField(max_length=255)                    # 用例集名
    passs = models.CharField(max_length=255)                    # 用例集名
    cpu= models.CharField(max_length=255)                       # 用例集名
    memory= models.CharField(max_length=255)                    # 用例集名
    Battery= models.CharField(max_length=255)                   # 用例集名
    casetype= models.CharField(max_length=255)                  # 用例集名
    caseid= models.CharField(max_length=255)                    # 用例集名
    def __str__(self):
        return self.slave_name

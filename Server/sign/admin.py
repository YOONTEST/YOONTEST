from django.contrib import admin
from sign.models import *

# Register your models here.
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ['id','scenario_name','testcase_name','project_name']
    search_fields = ['id','scenario_name','testcase_name','project_name']    # 搜索功能
    list_filter = ['id','project_name']    # 过滤器

admin.site.register(Testcase, TestcaseAdmin)

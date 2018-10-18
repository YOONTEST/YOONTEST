"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from sign import views
from sign import views_if
from sign.view import plan_views
from sign.view import test_case_views
from sign.view import execution_views
from sign.view import search_views
from sign.view import report_views
from sign.view import repository_views
from sign.view import device_views
from api_v1 import setting
from api_v1 import test_data

router = routers.DefaultRouter()
router.register(r'Testcase',views_if.TestcaseViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^logout/$', views.logout),
    url(r'^login_action/$', views.login_action),
    url(r'^accounts/login/$', views.index),
    url(r'^home/$', views.home),
    url(r'^download_logs/$', views.download_logs),
    url(r'^report/(?P<type>.*)/$', report_views.report),
    url(r'^report_download/(?P<type>.*)/$', report_views.report_download),

    url(r'^repository/(?P<search_contents>.*)/$', search_views.search_element),
    url(r'^device/(?P<search_contents>.*)/$', search_views.search_device),
    url(r'^case/(?P<platform>.*)/(?P<search_contents>.*)/$', search_views.search_case),
    url(r'^test-plan/(?P<search_contents>.*)/$', search_views.search_plan),
    url(r'^caseplan-detail/(?P<plan_id>[0-9]+)/(?P<search_contents>.*)/$', search_views.search_plan_details),
    url(r'^edit_PlanRelation/(?P<plan_id>[0-9]+)/(?P<search_contents>.*)/$', search_views.search_plan_relation),

    url(r'^repository/$', repository_views.repositories),
    url(r'^element/(?P<action>.*)/(?P<element_key>.*)/$', repository_views.element),

    url(r'^device/$', device_views.device),
    url(r'^add_device/$', device_views.add_device),
    url(r'^add_device_action/$', device_views.add_device_action),
    url(r'^delete_device_action/(?P<device_id>[0-9]+)/$', device_views.delete_device_action),
    url(r'^edit_device/(?P<device_id>[0-9]+)/$', device_views.edit_device),
    url(r'^view_device/(?P<device_id>[0-9]+)/$', device_views.view_device),
    url(r'^edit_device_action/$', device_views.edit_device_action),

    url(r'^case/(?P<platform>.*)/$', test_case_views.case),
    url(r'^add_case/(?P<platform>.*)/$', test_case_views.add_case),
    url(r'^add_case_action/$', test_case_views.add_case_action),
    url(r'^edit_case/(?P<testcase_id>[0-9]+)/$', test_case_views.edit_case),
    url(r'^edit_case_action/$', test_case_views.edit_case_action),
    url(r'^view_case/(?P<testcase_id>[0-9]+)/$', test_case_views.view_case),
    url(r'^delete_case_action/(?P<testcase_id>[0-9]+)/$', test_case_views.delete_case_action),
    url(r'^run_api_script/(?P<case_id>.*)/$', test_case_views.run_api_script),
    url(r'^step_api/(?P<action>.*)/(?P<case_id>[0-9]+)/(?P<step_id>[0-9]+)/$', test_case_views.step_api),
    url(r'^step_web/(?P<action>.*)/(?P<case_id>[0-9]+)/(?P<step_id>[0-9]+)/$', test_case_views.step_web),
    url(r'^step_app/(?P<action>.*)/(?P<case_id>[0-9]+)/(?P<step_id>[0-9]+)/$', test_case_views.step_app),

    url(r'^test-plan/$', plan_views.test_plan),
    url(r'^add_test_plan/$', plan_views.add_test_plan),
    url(r'^view_test_plan/(?P<plan_id>.*)/$', plan_views.view_test_plan),
    url(r'^add_test_plan_action/$', plan_views.add_test_plan_action),
    url(r'^edit_test_plan/(?P<plan_id>.*)/$', plan_views.edit_test_plan),
    url(r'^edit_test_plan_action/$', plan_views.edit_test_plan_action),
    url(r'^delete_test_plan_action/(?P<plan_id>.*)/$', plan_views.delete_test_plan_action),
    url(r'^delete_CasePlanRelation_action/(?P<plan_id>[0-9]+)/$', plan_views.delete_CasePlanRelation_action),
    url(r'^delete_CasePlanRelation_action_s/(?P<plan_id>[0-9]+)/(?P<id>[0-9]+)/$', plan_views.delete_CasePlanRelation_action_s),
    url(r'^edit_PlanRelation/(?P<plan_id>[0-9]+)/$', plan_views.Case_checkbox),
    url(r'^edit_PlanRelation_submit/(?P<plan_id>[0-9]+)/$', plan_views.Case_checkbox_submit),
    url(r'^caseplan-detail/(?P<plan_id>[0-9]+)/$', plan_views.caseplan_detail),

    url(r'^execution/$', execution_views.execution),
    url(r'^run_scripts/$', execution_views.run_scripts),
    url(r'^run_results/(?P<activity_id>[0-9]+)/$', execution_views.run_results),
    url(r'^rerun_scripts/(?P<activity_id>[0-9]+)/$', execution_views.rerun_scripts),
    url(r'^delete_scripts/(?P<activity_id>[0-9]+)/$', execution_views.delete_scripts),
    
    url(r'^test-case/', test_data.get_test_case),
    url(r'^run-list/', test_data.get_run_list),
    url(r'^get-activity/', test_data.get_activity),
    url(r'^get-device/', test_data.get_device),
    url(r'^set-activity/', test_data.set_activity),
    url(r'^slave/', test_data.slave),
    url(r'^upload-run-data/', test_data.upload_run_time),
    url(r'^get_run_data/', test_data.get_run_time),
    url(r'^upload-result/', test_data.upload_results),
    url(r'^get-setting/', setting.get),
]

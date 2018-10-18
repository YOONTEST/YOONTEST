from django.conf.urls import url
from sign import views_if,views_if_sec

urlpatterns = [
    # guest system interface:
    # ex : /api/add_event/
    url(r'^add_testcase/', views_if.add_testcase, name='add_testcase'),
    # ex : /api/get_guest_list/
    url(r'^get_testcase/', views_if.get_testcase, name='get_testcase'),

    # security interface:
    # ex : /api/sec_get_event_list/
    url(r'^sec_get_testcase/', views_if_sec.get_testcase, name='get_testcase'),
    # ex : /api/sec_add_event/
    url(r'^sec_add_testcase/', views_if_sec.add_testcase, name='add_testcase'),
    # ex : /api/sec_get_guest_list/
    #url(r'^sec_get_guest_list/', views_if_sec.get_guest_list, name='get_guest_list'),
]

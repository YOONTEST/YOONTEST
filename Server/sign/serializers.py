from django.contrib.auth.models import User, Group
from rest_framework import serializers
from sign.models import Testcase

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','email','groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')

class TestcaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Testcase
        fields = ('scenario_name','testcase_name','project_id','project_name','create_time')

from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'fio', 'position', 'salary_by_hour', 'firstday', 'salary_sum', 'boss']

from rest_framework import serializers
from apps.payroll.models import (
    PayrollPeriod,
    PayrollConcept,
    Payroll,
    Deduction,
    Income,
)

class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = '__all__'


class PayrollConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollConcept
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
from django.shortcuts import render

# models
from apps.employee.models import Department, JobPosition, Employee, FamilyMember, SalaryIncrease
from app.payroll.models import PayrollPeriod, PayrollConcept, Payroll, Deduction, Income

# serializers
from apps.payroll.serializers import PayrollSerializer, PayrollPeriodSerializer, PayrollConceptSerializer, DeductionSerializer, IncomeSerializer

# rest_framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
# import datetime
from datetime import date

class PayrollPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer

class PayrollConceptViewSet(viewsets.ModelViewSet):
    queryset = PayrollConcept.objects.all()
    serializer_class = PayrollConceptSerializer

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

    @action(detail=False, methods=['post'])
    def generate_payroll(self, request):
        payroll_period = request.data.get('payroll_period')
        try:
            payroll_period = PayrollPeriod.objects.get(pk=payroll_period)
        except PayrollPeriod.DoesNotExist:
            return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        employees = Employee.objects.filter(is_active=True)
        for employee in employees:
            total_salary = employee.calculte_total_salary()
            payroll = Payroll.objects.create(
                employee=employee,
                payroll_period=payroll_period,
                data_generated=date.today(),
                total=total_salary,
                status_payroll="Pendiente"
            )
            payroll.save()

        return Response({'message': 'Planilla generada correctamente'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def pay_payroll(self, request):
        payroll = request.data.get('payroll')
        try:
            payroll = Payroll.objects.get(pk=payroll)
        except Payroll.DoesNotExist:
            return Response({'message': 'Planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        payroll.status_payroll = "Pagada"
        payroll.save()

        return Response({'message': 'Planilla pagada correctamente'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def get_payroll_by_employee(self, request):
        employee = request.data.get('employee')
        try:
            employee = Employee.objects.get(pk=employee)
        except Employee.DoesNotExist:
            return Response({'message': 'Empleado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        payrolls = Payroll.objects.filter(employee=employee)
        serializer = PayrollSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def get_payroll_by_payroll_period(self, request):
        payroll_period = request.data.get('payroll_period')
        try:
            payroll_period = PayrollPeriod.objects.get(pk=payroll_period)
        except PayrollPeriod.DoesNotExist:
            return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        payrolls = Payroll.objects.filter(payroll_period=payroll_period)
        serializer = PayrollSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer



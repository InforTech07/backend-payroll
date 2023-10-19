from django.shortcuts import render

# models
from apps.employee.models import Employee
from apps.payroll.models import (
                                PayrollPeriod, 
                                Payroll, 
                                PayrollDeduction, 
                                PayrollIncome, 
                                PayrollAccountingTransaction,
                                PayrollConcept,
                            )

# serializers
from apps.payroll.serializers import (
                                PayrollSerializer, 
                                PayrollPeriodSerializer, 
                                PayrollDeductionSerializer,
                                PayrollIncomeSerializer,
                                PayrollAccountingTransactionSerializer,
                                PayrollConceptSerializer,
                                )

# rest_framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
# import datetime
from datetime import date

class PayrollPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer

    @action(detail=False, methods=['get'])
    def get_payroll_periods(self, request):
        payroll_periods = PayrollPeriod.objects.filter(company=request.query_params.get('company'))
        serializer = PayrollPeriodSerializer(payroll_periods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

    @action(detail=False, methods=['get'])
    def get_payrolls(self,request):
        payrolls = Payroll.objects.filter(company=request.query_params.get('company'))
        serializer = PayrollSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def generate_prev_payroll(self, request):
        payroll_period_id = request.query_params.get('payroll_period')
        company_id = request.query_params.get('company')
        try:
            payroll_period_instance = PayrollPeriod.objects.get(id=payroll_period_id)
            if payroll_period_instance is None:
                return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
            employees = Employee.objects.filter(is_active=True, company=company_id)
            payroll_prev = []
            for employee in employees:
                result = employee.get_calculate_payroll(payroll_period_instance)
                payroll = Payroll()
                payroll.employee_name = employee.first_name + ' ' + employee.last_name
                payroll.employee = employee
                payroll.gross_salary = result['gross_salary']
                payroll.net_salary = result['net_salary']
                payroll.incomes = result['total_income']
                payroll.deductions = result['total_deduction']
                payroll.social_insurance_employee = result['social_insurance_employee']
                payroll.social_insurance_company = result['social_insurance_company']
                payroll.gross_biweekly_salary = result['gross_biweekly_salary']
                payroll.net_biweekly_salary = result['net_biweekly_salary']
                payroll.total_biweekly_deduction = result['total_biweekly_deduction']
                payroll.salary_base = employee.base_salary
                payroll.payroll_period = payroll_period_instance
                payroll_prev.append(payroll)
                
            serializer = PayrollSerializer(payroll_prev, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PayrollPeriod.DoesNotExist:
            return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def generate_prev_payrolll(self, request):
        payroll_period_id = request.query_params.get('payroll_period')
        company_id = request.query_params.get('company')
        try:
            payroll_period_instance = PayrollPeriod.objects.get(id=payroll_period_id)
            if payroll_period_instance is None:
                return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
            type_period = payroll_period_instance.type
            if type_period == 'QUINCENAL':
                employees = Employee.objects.filter(is_active=True, company=company_id)
                payroll_prev = []
                for employee in employees:
                    result = employee.calculte_biweekly_payroll(payroll_period_instance)
                    payroll = Payroll()
                    payroll.employee_name = employee.first_name + ' ' + employee.last_name
                    payroll.employee = employee
                    payroll.total = result['total_salary']
                    payroll.incomes = result['total_income']
                    payroll.deductions = result['total_deduction']
                    payroll.salary_base = employee.base_salary
                    payroll.social_insurance_employee = result['social_insurance_employee']
                    payroll.social_insurance_company = result['social_insurance_company']
                    payroll.payroll_period = payroll_period_instance
                    payroll_prev.append(payroll)
                serializer = PayrollSerializer(payroll_prev, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                employees = Employee.objects.filter(is_active=True, company=company_id)
                payroll_prev = []
                for employee in employees:
                    result = employee.get_calculate_payroll(payroll_period_instance)
                    print(result)
                    payroll = Payroll()
                    payroll.employee_name = employee.first_name + ' ' + employee.last_name
                    payroll.employee = employee
                    payroll.gross_salary = result['gross_salary']
                    payroll.net_salary = result['net_salary']
                    payroll.incomes = result['total_income']
                    payroll.deductions = result['total_deduction']
                    payroll.social_insurance_employee = result['social_insurance_employee']
                    payroll.social_insurance_company = result['social_insurance_company']
                    payroll.gross_biweekly_salary = result['gross_biweekly_salary']
                    payroll.net_biweekly_salary = result['net_biweekly_salary']
                    payroll.total_biweekly_deduction = result['total_biweekly_deduction']
                    payroll.salary_base = employee.base_salary
                    payroll.payroll_period = payroll_period_instance
                    payroll_prev.append(payroll)
                serializer = PayrollSerializer(payroll_prev, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except PayrollPeriod.DoesNotExist:
            return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)

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
    def generate_payroll_bono14(self, request):
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
    
    #@action(detail=False, methods=['get'])
    # def get_biweekly_payroll(self, request):
    #     payroll_period = request.query_params.get('payroll_period')
    #     company_id = request.query_params.get('company')
    #     try:
    #         payroll_period_instance = PayrollPeriod.objects.get(pk=payroll_period)
    #         employees = Employee.objects.filter(is_active=True)
    #         payroll_prev = []
    #         for employee in employees:
    #             result = employee.calculte_biweekly_payroll(payroll_period)
    #             payroll = Payroll()
    #             payroll.employee_name = employee.first_name + ' ' + employee.last_name
    #             payroll.employee = employee
    #             payroll.total = result['total_salary']
    #             payroll.incomes = result['total_income']
    #             payroll.deductions = result['total_deduction']
    #             payroll.salary_base = employee.base_salary
    #             payroll.social_insurance_employee = result['social_insurance_employee']
    #             payroll.social_insurance_company = result['social_insurance_company']
    #             payroll.payroll_period = payroll_period_instance
    #             payroll_prev.append(payroll)
    #         serializer = PayrollSerializer(payroll_prev, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except PayrollPeriod.DoesNotExist:
    #         return Response({'message': 'Periodo de planilla no existe'}, status=status.HTTP_400_BAD_REQUEST)
        

    

class PayrollDeductionViewSet(viewsets.ModelViewSet):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer

class PayrollIncomeViewSet(viewsets.ModelViewSet):
    queryset = PayrollIncome.objects.all()
    serializer_class = PayrollIncomeSerializer

class PayrollAccountingTransactionViewSet(viewsets.ModelViewSet):
    queryset = PayrollAccountingTransaction.objects.all()
    serializer_class = PayrollAccountingTransactionSerializer

class PayrollConceptViewSet(viewsets.ModelViewSet):
    queryset = PayrollConcept.objects.filter(is_active=True)
    serializer_class = PayrollConceptSerializer

    @action(detail=False, methods=['get'])
    def get_payroll_concepts_by_company(self, request):
        payroll_concepts = PayrollConcept.objects.filter(is_active=True, company=request.query_params.get('company'))
        serializer = PayrollConceptSerializer(payroll_concepts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
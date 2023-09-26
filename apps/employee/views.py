from django.shortcuts import render

# models
from apps.employee.models import Department, JobPosition, Employee, FamilyMember, SalaryIncrease

# serializers
from apps.employee.serializers import DepartmentSerializer, JobPositionSerializer, EmployeeSerializer, FamilyMemberSerializer, SalaryIncreaseSerializer


# rest_framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer

    #get department by company
    # def department_by_company(self, request, pk=None):
    #     try:
    #         department = Department.objects.filter(company=pk)
    #         serializer = DepartmentSerializer(department, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.filter(is_active=True)
    serializer_class = JobPositionSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['post'])
    def calculte_salary(self, request):
        print(request.data)
        employee = request.data.get('employee')
        try:
            employee = Employee.objects.get(pk=employee)
        except Employee.DoesNotExist:
            return Response({'message': 'Empleado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_salary = employee.calculte_total_salary()
        return Response({'total_salary': total_salary}, status=status.HTTP_200_OK)

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.filter(is_active=True)
    serializer_class = FamilyMemberSerializer


class SalaryIncreaseViewSet(viewsets.ModelViewSet):
    queryset = SalaryIncrease.objects.filter(is_active=True)
    serializer_class = SalaryIncreaseSerializer
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Departamento eliminado correctamente'}, status=status.HTTP_200_OK)

        



class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.filter(is_active=True)
    serializer_class = JobPositionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Puesto eliminado correctamente'}, status=status.HTTP_200_OK)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def get_employees(self, request):
        employees = Employee.objects.filter(is_active=True, company=request.query_params.get('company'))
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Empleado eliminado correctamente'}, status=status.HTTP_200_OK)

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
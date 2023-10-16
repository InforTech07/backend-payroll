from django.shortcuts import render

# models
from apps.employee.models import (
                            Department, 
                            JobPosition, 
                            Employee, 
                            FamilyMember, 
                            SalaryIncrease, 
                            EmployeeDocument,
                            RequestAbsence
                            )

# serializers
from apps.employee.serializers import (
                DepartmentSerializer, 
                JobPositionSerializer, 
                EmployeeSerializer, 
                FamilyMemberSerializer, 
                SalaryIncreaseSerializer, 
                EmployeeDocumentSerializer,
                RequestAbsenceSerializer
            )


# rest_framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'])
    def get_departments_by_company(self, request):
        departments = Department.objects.filter(is_active=True, company=request.query_params.get('company'))
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Departamento eliminado correctamente'}, status=status.HTTP_200_OK)


class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.filter(is_active=True)
    serializer_class = JobPositionSerializer

    @action(detail=False, methods=['get'])
    def get_job_positions_by_company(self, request):
        job_positions = JobPosition.objects.filter(is_active=True, company=request.query_params.get('company'))
        serializer = JobPositionSerializer(job_positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

    @action(detail=False, methods=['get'])
    def get_family_members(self, request):
        family_members = FamilyMember.objects.filter(is_active=True, employee=request.query_params.get('employee'))
        serializer = FamilyMemberSerializer(family_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalaryIncreaseViewSet(viewsets.ModelViewSet):
    queryset = SalaryIncrease.objects.filter(is_active=True)
    serializer_class = SalaryIncreaseSerializer

class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDocument.objects.filter(is_active=True)
    serializer_class = EmployeeDocumentSerializer

    @action(detail=False, methods=['get'])
    def get_documents(self, request):
        documents = EmployeeDocument.objects.filter(is_active=True, employee=request.query_params.get('employee'))
        serializer = EmployeeDocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Documento eliminado correctamente'}, status=status.HTTP_200_OK)
    
class RequestAbsenceViewSet(viewsets.ModelViewSet):
    queryset = RequestAbsence.objects.filter(is_active=True)
    serializer_class = RequestAbsenceSerializer

    @action(detail=False, methods=['get'])
    def get_requests(self, request):
        requests = RequestAbsence.objects.filter(is_active=True, employee=request.query_params.get('employee'))
        serializer = RequestAbsenceSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Solicitud eliminada correctamente'}, status=status.HTTP_200_OK)
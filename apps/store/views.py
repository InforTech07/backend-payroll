from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import StorePurchase
from apps.employee.models import Employee
from .serializers import StorePurchaseSerializer

class StorePurchaseViewSet(viewsets.ModelViewSet):
    """
    StorePurchase viewset.
    """
    queryset = StorePurchase.objects.all()
    serializer_class = StorePurchaseSerializer

    @action(detail=False, methods=['post'])
    def create_credit(self, request):
        """
        Create a store purchase.
        """
        employee = Employee.objects.get(user=request.data['user'])
        request.data['employee'] = employee.id
        request.data['base_salary'] = employee.base_salary
        print(request.data)
        
        serializer = StorePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
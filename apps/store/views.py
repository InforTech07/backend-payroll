from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import StorePurchase
from .serializers import StorePurchaseSerializer

class StorePurchaseViewSet(viewsets.ModelViewSet):
    """
    StorePurchase viewset.
    """
    queryset = StorePurchase.objects.all()
    serializer_class = StorePurchaseSerializer

    @action(detail=False, methods=['get'])
    def get_store_purchases_by_company(self, request):
        """
        Get all store purchases.
        """
        sales = StorePurchase.objects.filter(company=request.query_params['company'])
        serializer = StorePurchaseSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def create_credit(self, request):
    #     """
    #     Create a store purchase.
    #     """
    #     employee = Employee.objects.get(user=request.data['user'])
    #     request.data['employee'] = employee.id
    #     request.data['base_salary'] = employee.base_salary
    #     print(request.data)
        
    #     serializer = StorePurchaseSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
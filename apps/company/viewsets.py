""" Company Viewsets"""

#Django rest framework
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


#Models
from apps.company.models import Company
from apps.user.models import User

#Serializers
from apps.company.serializers import CompanySerializer
#from apps.user.serializers import UserAccountSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company viewset.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    #permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the companies
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Company.objects.filter(company_user=user)

    # def create(self, request, *args, **kwargs):
    #     """
    #     Create a company.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     company = serializer.save()
    #     data = CompanySerializer(company).data
    #     return Response(data, status=status.HTTP_201_CREATED)

    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     Update a company.
    #     """
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     company = serializer.save('partial')
    #     data = CompanySerializer(company).data
    #     return Response(data, status=status.HTTP_200_OK)



    # def update(self, request, *args, **kwargs):
    #     """
    #     Update a company.
    #     """
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     company = serializer.save()
    #     data = CompanySerializer(company).data
    #     return Response(data, status=status.HTTP_200_OK)

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Delete a company.
    #     """
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
"""
    urls for company 
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import CompanyViewSet


router = DefaultRouter()
router.register(r'company', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


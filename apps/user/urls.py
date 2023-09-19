"""
    urls for user
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
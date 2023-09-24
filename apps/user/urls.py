"""
    urls for user
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet, UserLoginViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'login', UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]
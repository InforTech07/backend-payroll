"""Media urls."""
from django.urls import path, include


from rest_framework.routers import DefaultRouter
from .viewsets import PayrollImageViewSet, PayrollFileViewSet

router = DefaultRouter()
router.register("image", PayrollImageViewSet)
router.register("file", PayrollFileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
from rest_framework.routers import DefaultRouter
from apps.store.views import StorePurchaseViewSet
from django.urls import path, include

# department_by_company = DepartmentViewSet.as_view({
#     'get': 'department_by_company',
# })


router = DefaultRouter()
router.register(r'store_purchase', StorePurchaseViewSet, basename='store_purchase')



urlpatterns = [
    path('', include(router.urls)),
]
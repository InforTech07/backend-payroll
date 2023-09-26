"""
payroll app url
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.payroll.views import PayrollPeriodViewSet, PayrollConceptViewSet, PayrollViewSet, DeductionViewSet, IncomeViewSet

# department_by_company = DepartmentViewSet.as_view({
#     'get': 'department_by_company',
# })


router = DefaultRouter()
router.register(r'payroll_period', PayrollPeriodViewSet, basename='payroll_period')
router.register(r'payroll_concept', PayrollConceptViewSet, basename='payroll_concept')
router.register(r'payroll', PayrollViewSet, basename='payroll')
router.register(r'deduction', DeductionViewSet, basename='deduction')
router.register(r'income', IncomeViewSet, basename='income')



urlpatterns = [
    path('', include(router.urls)),
]


"""
payroll app url
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.payroll.views import (
                                PayrollPeriodViewSet, 
                                PayrollViewSet, 
                                PayrollDeductionViewSet, 
                                PayrollIncomeViewSet,
                                PayrollAccountingTransactionViewSet,
                                PayrollConceptViewSet,
                            )

# department_by_company = DepartmentViewSet.as_view({
#     'get': 'department_by_company',
# })


router = DefaultRouter()
router.register(r'payroll_period', PayrollPeriodViewSet, basename='payroll_period')
router.register(r'payroll', PayrollViewSet, basename='payroll')
router.register(r'payroll_deduction', PayrollDeductionViewSet, basename='payroll_deduction')
router.register(r'payroll_income', PayrollIncomeViewSet, basename='payroll_income')
router.register(r'payroll_accounting_transaction', PayrollAccountingTransactionViewSet, basename='payroll_accounting_transaction')
router.register(r'payroll_concept', PayrollConceptViewSet, basename='payroll_concept')



urlpatterns = [
    path('', include(router.urls)),
]


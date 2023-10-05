"""
emploryee app url
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.employee.views import (
                        DepartmentViewSet, 
                        JobPositionViewSet, 
                        EmployeeViewSet, 
                        FamilyMemberViewSet, 
                        SalaryIncreaseViewSet, 
                        EmployeeDocumentViewSet,
                        OvertimeViewSet,
                        SalesCommissionViewSet,
                        ProductionBonusViewSet,
                        )

# department_by_company = DepartmentViewSet.as_view({
#     'get': 'department_by_company',
# })


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename='department')
# router.register(r'department-by-company', DepartmentViewSet.department_by_company, basename='department-by-company')
router.register(r'job-position', JobPositionViewSet, basename='job-position')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'employee-document', EmployeeDocumentViewSet, basename='employee-document')
router.register(r'family-member', FamilyMemberViewSet, basename='family-member')
router.register(r'salary-increase', SalaryIncreaseViewSet, basename='salary-increase')
router.register(r'overtime', OvertimeViewSet, basename='overtime')
router.register(r'sales-commission', SalesCommissionViewSet, basename='sales-commission')
router.register(r'production-bonus', ProductionBonusViewSet, basename='production-bonus')


urlpatterns = [
    path('', include(router.urls)),
]



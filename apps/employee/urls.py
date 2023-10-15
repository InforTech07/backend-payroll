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
                        )

# department_by_company = DepartmentViewSet.as_view({
#     'get': 'department_by_company',
# })


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename='department')
# router.register(r'department-by-company', DepartmentViewSet.department_by_company, basename='department-by-company')
router.register(r'job-position', JobPositionViewSet, basename='job-position')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'employee_document', EmployeeDocumentViewSet, basename='employee_document')
router.register(r'family_member', FamilyMemberViewSet, basename='family_member')
router.register(r'salary_increase', SalaryIncreaseViewSet, basename='salary_increase')

urlpatterns = [
    path('', include(router.urls)),
]



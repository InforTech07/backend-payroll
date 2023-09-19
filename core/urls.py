"""core URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.company.urls')),
    path('api/v1/', include('apps.user.urls')),
    #path('api/v1/', include('apps.employee.urls')),
    #path('api/v1/', include('apps.payroll.urls')),
    #path('api/v1/', include('apps.store.urls')),
    path('api/v1/media/', include('apps.media.urls')),
]

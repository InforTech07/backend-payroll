"""core URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# DRF_YASG
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Payroll API",
        default_version='v1',
        description="Api-rest para el manejo de la nomina de una empresa",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="suport@payroll.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.company.urls')),
    path('api/v1/', include('apps.user.urls')),
    path('api/v1/', include('apps.employee.urls')),
    path('api/v1/', include('apps.payroll.urls')),
    path('api/v1/media/', include('apps.media.urls')),
    path('api/v1/', include('apps.store.urls')),
    path('api/v1/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

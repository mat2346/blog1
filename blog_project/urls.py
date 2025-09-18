"""
URL configuration for blog_project project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración del esquema de documentación
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="API completa para la gestión de blogs con autenticación JWT",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="Equipo de Desarrollo",
            email="contacto@blog.com"
        ),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # APIs del proyecto
    path('api/usuarios/', include('usuarios.urls')),
    path('api/blog/', include('blog.urls')), 
    path('api/post/', include('post.urls')),
    
    # Documentación de la API
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-alt'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Esquemas JSON/YAML
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

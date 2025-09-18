from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, PostViewSet, LikePostViewSet, ComentarioViewSet, EtiquetaViewSet, PostEtiquetaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikePostViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'etiquetas', EtiquetaViewSet)
router.register(r'post-etiquetas', PostEtiquetaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
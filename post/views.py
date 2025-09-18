from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Post, LikePost, Comentario, Etiqueta, PostEtiqueta
from .serializers import CategoriaSerializer, PostSerializer, LikePostSerializer, ComentarioSerializer, EtiquetaSerializer, PostEtiquetaSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from blog_project.permissions import SuperuserOrAuthenticated

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [SuperuserOrAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [SuperuserOrAuthenticated]
    
    def get_queryset(self):
        queryset = Post.objects.all()
        blog_id = self.request.query_params.get('blog_id')
        categoria_id = self.request.query_params.get('categoria_id')
        
        if blog_id:
            queryset = queryset.filter(blog_id=blog_id)
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)
        
        return queryset
    
    @swagger_auto_schema(
        operation_description="Dar like o quitar like a un post",
        responses={
            200: openapi.Response(description='Like eliminado correctamente'),
            201: openapi.Response(description='Like agregado correctamente')
        }
    )
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        post = self.get_object()
        user = request.user
        
        # Verifica si ya existe un like
        like_exists = LikePost.objects.filter(usuario=user, post=post).exists()
        
        if like_exists:
            # Si ya existe, elimina el like (toggle)
            LikePost.objects.filter(usuario=user, post=post).delete()
            return Response({'status': 'like removed'}, status=status.HTTP_200_OK)
        else:
            # Si no existe, crea un nuevo like
            like = LikePost(usuario=user, post=post)
            like.save()
            return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)

class LikePostViewSet(viewsets.ModelViewSet):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = [SuperuserOrAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return LikePost.objects.filter(usuario=self.request.user)
        return LikePost.objects.none()
        
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [SuperuserOrAuthenticated]
    
    def get_queryset(self):
        # Filtra comentarios por post si se especifica
        queryset = Comentario.objects.all()
        post_id = self.request.query_params.get('post_id')
        solo_principales = self.request.query_params.get('solo_principales')
        
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Si solo_principales=true, solo devuelve comentarios que no son respuestas
        if solo_principales and solo_principales.lower() == 'true':
            queryset = queryset.filter(comentario_padre__isnull=True)
            
        return queryset.order_by('-fecha_creacion')
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [SuperuserOrAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Obtener todos los posts asociados a una etiqueta",
        responses={200: PostSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        etiqueta = self.get_object()
        posts = Post.objects.filter(post_etiquetas__etiqueta=etiqueta)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = PostEtiqueta.objects.all()
    serializer_class = PostEtiquetaSerializer
    permission_classes = [SuperuserOrAuthenticated]
    
    def get_queryset(self):
        queryset = PostEtiqueta.objects.all()
        post_id = self.request.query_params.get('post_id')
        etiqueta_id = self.request.query_params.get('etiqueta_id')
        
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        if etiqueta_id:
            queryset = queryset.filter(etiqueta_id=etiqueta_id)
            
        return queryset.order_by('-fecha')
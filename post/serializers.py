from rest_framework import serializers
from .models import Categoria, Post, LikePost, Comentario, Etiqueta, PostEtiqueta
from django.conf import settings

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comentarios_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'titulo', 'contenido', 'blog', 'categoria', 'fecha_creacion', 
                 'fecha_actualizacion', 'likes_count', 'comentarios_count']
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comentarios_count(self, obj):
        return obj.comentarios.count()

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'usuario', 'post', 'fecha']
        read_only_fields = ['usuario', 'fecha']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['usuario'] = request.user
        else:
            raise serializers.ValidationError("Authentication required")
        return super().create(validated_data)

class ComentarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    respuestas = serializers.SerializerMethodField()
    es_respuesta = serializers.SerializerMethodField()
    
    class Meta:
        model = Comentario
        fields = ['id', 'contenido', 'usuario', 'usuario_nombre', 'post', 'comentario_padre', 
                 'fecha_creacion', 'fecha_actualizacion', 'respuestas', 'es_respuesta']
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_respuestas(self, obj):
        # Obtiene las respuestas del comentario (comentarios hijos)
        if obj.respuestas.exists():
            return ComentarioSerializer(obj.respuestas.all(), many=True, context=self.context).data
        return []
    
    def get_es_respuesta(self, obj):
        # Indica si este comentario es una respuesta a otro comentario
        return obj.comentario_padre is not None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['usuario'] = request.user
        else:
            raise serializers.ValidationError("Authentication required")
        return super().create(validated_data)


class EtiquetaSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre', 'posts_count']
    
    def get_posts_count(self, obj):
        return obj.post_etiquetas.count()


class PostEtiquetaSerializer(serializers.ModelSerializer):
    etiqueta_nombre = serializers.CharField(source='etiqueta.nombre', read_only=True)
    post_titulo = serializers.CharField(source='post.titulo', read_only=True)
    
    class Meta:
        model = PostEtiqueta
        fields = ['id', 'post', 'post_titulo', 'etiqueta', 'etiqueta_nombre', 'fecha']
        read_only_fields = ['fecha']
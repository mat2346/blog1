
from django.contrib import admin
from .models import Categoria, Post, LikePost, Comentario, Etiqueta, PostEtiqueta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'blog', 'fecha_creacion']
    list_filter = ['categoria', 'blog']
    search_fields = ['titulo', 'contenido']
    filter_horizontal = ['categoria']

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'post', 'fecha']
    list_filter = ['fecha']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'post', 'comentario_padre', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido']

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(PostEtiqueta)
class PostEtiquetaAdmin(admin.ModelAdmin):
    list_display = ['post', 'etiqueta', 'fecha']
    list_filter = ['fecha', 'etiqueta']


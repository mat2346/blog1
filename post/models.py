from django.db import models
from django.conf import settings
from blog.models import Blog  # Importa el modelo Blog desde la app blog

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    
class Post(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    blog = models.ForeignKey(
        Blog,  # Referencia con formato 'app_name.ModelName'
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categoria = models.ManyToManyField(
        Categoria,
        related_name='posts'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-fecha_creacion']
  

class LikePost(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario} - {self.post}"


class Comentario(models.Model):
    contenido = models.TextField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    comentario_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comentario de {self.usuario} en {self.post}"
    
    class Meta:
        ordering = ['-fecha_creacion']


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']


class PostEtiqueta(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_etiquetas'
    )
    etiqueta = models.ForeignKey(
        Etiqueta,
        on_delete=models.CASCADE,
        related_name='post_etiquetas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'etiqueta')
    
    def __str__(self):
        return f"{self.post} - {self.etiqueta}"

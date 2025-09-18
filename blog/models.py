from django.db import models
from django.conf import settings

class Blog(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    url_foto_portada = models.URLField(max_length=500, blank=True, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs'
    )

    def __str__(self):
        return self.titulo

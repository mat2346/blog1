from django.db import models
from cloudinary.models import CloudinaryField

# class Permiso(models.Model):
#     nombre = models.CharField(max_length=50)
#     descripcion = models.TextField()
    
#     def __str__(self):
#         return self.nombre
    
# class Usuario(models.Model):
#     nombre = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)     
#     # url_foto_de_perfil = models.URLField()
#     suspendido = models.BooleanField(default=False) 
    
#     def __str__(self):
        
#         return self.nombre 
# class Blog(models.Model):   
#     titulo = models.CharField(max_length=50)
#     descripcion = models.TextField()
#     # url_foto_de_perfil = models.URLField()        
#     def __str__(self):
#         return self.titulo
# class Categoria(models.Model):
#     nombre = models.CharField(max_length=50)
#     descripcion = models.TextField()
        
#     def __str__(self):
#         return self.nombre    

# class Post(models.Model):       
#     titulo = models.CharField(max_length=50)
#     contenido = models.TextField()
    
#     def __str__(self):
#         return self.titulo

# class Etiqueta(models.Model):
#     nombre = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.nombre
    
# class Post_Etiqueta(models.Model):   
#     fecha = models.DateTimeField(auto_now_add=True)
    
# class Comentario(models.Model):
#     comentario = models.TextField()             
#     fecha = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.comentario[:100]
    
# class Like_Post(models.Model):
#     fecha = models.DateTimeField(auto_now_add=True)
    
# class Like_Comentario(models.Model):
#     fecha = models.DateTimeField(auto_now_add=True)
    
# class Bitacora(models.Model):
#     fecha = models.DateTimeField(auto_now_add=True)
#     actividad = models.TextField()
    
#     def __str__(self):
#         return self.actividad[:100]
    
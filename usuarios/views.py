from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from .models import Usuario
from .serializers import UsuarioSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import DjangoModelPermissions

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar usuarios.
    Permite listar, crear, ver, actualizar y eliminar usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """
        Permisos personalizados basados en la acción:
        - list: Solo administradores
        - retrieve: Usuario propio o administradores
        - create: Cualquiera puede registrarse
        - update/partial_update: Usuario propio o administradores
        - destroy: Solo administradores
        - superusuarios tienen acceso completo sin autenticación
        """
        from blog_project.permissions import SuperuserOrAuthenticated
        
        permission_map = {
            'list': [SuperuserOrAuthenticated(), DjangoModelPermissions()],
            'create': [permissions.AllowAny()],  # Mantener AllowAny para registro
            'retrieve': [SuperuserOrAuthenticated()],
            'update': [SuperuserOrAuthenticated(), DjangoModelPermissions()],
            'partial_update': [SuperuserOrAuthenticated(), DjangoModelPermissions()],
            'destroy': [SuperuserOrAuthenticated(), DjangoModelPermissions()]
        }
        return permission_map.get(self.action, [SuperuserOrAuthenticated()])
    
    def get_queryset(self):
        """
        Filtrar el queryset según el usuario:
        - Administradores ven todos los usuarios
        - Usuarios normales solo se ven a sí mismos
        """
        if self.request.user.is_staff:
            return Usuario.objects.all()
        elif self.request.user.is_authenticated:
            return Usuario.objects.filter(id=self.request.user.id)
        return Usuario.objects.none()

class ChangePasswordView(generics.UpdateAPIView):
    """
    API endpoint para cambiar la contraseña.
    Requiere estar autenticado y proporcionar la contraseña actual.
    Superusuarios tienen acceso sin autenticación.
    """
    serializer_class = ChangePasswordSerializer
    
    def get_permissions(self):
        from blog_project.permissions import SuperuserOrAuthenticated
        return [SuperuserOrAuthenticated()]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Contraseña actual incorrecta."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Contraseña cambiada correctamente."})

class LogoutView(APIView):
    """
    API endpoint para cerrar sesión.
    Añade el token de refresco a la lista negra para invalidarlo.
    Superusuarios tienen acceso sin autenticación.
    """
    def get_permissions(self):
        from blog_project.permissions import SuperuserOrAuthenticated
        return [SuperuserOrAuthenticated()]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "El token de refresco es requerido"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Sesión cerrada correctamente"}, 
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {"error": "Token inválido o expirado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint para obtener tokens JWT.
    Usa el campo 'nombre' como identificador en lugar de 'username'.
    """
    serializer_class = CustomTokenObtainPairSerializer
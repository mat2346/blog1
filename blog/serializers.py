from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    url_foto_portada = serializers.URLField(
        required=False, 
        allow_blank=True, 
        allow_null=True,
        help_text="URL de la imagen de portada (opcional)"
    )
    
    class Meta:
        model = Blog
        fields = ['id', 'titulo', 'descripcion', 'url_foto_portada', 'usuario']
        read_only_fields = ['usuario']
        extra_kwargs = {
            'url_foto_portada': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
            }
        }

    def create(self, validated_data):
        # Asigna automáticamente el usuario autenticado al crear un blog
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['usuario'] = request.user
        else:
            raise serializers.ValidationError("Authentication required")
        return super().create(validated_data)
from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'descripcion', 'categoria', 'anio_publicacion', 'imagen_url']

class LibroDetalleSerializer(LibroSerializer):
    informacion_complementaria = serializers.SerializerMethodField() 

    class Meta(LibroSerializer.Meta):
        fields = LibroSerializer.Meta.fields + ['informacion_complementaria']
        
    def get_informacion_complementaria(self, obj):
        from .utils import obtener_datos_api_externa 
        
        try:
            return obtener_datos_api_externa(obj.titulo)
        except Exception:
            return "Información complementaria no disponible"
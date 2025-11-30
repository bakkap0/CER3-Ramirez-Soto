from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripción breve")
    categoria = models.CharField(max_length=100)
    anio_publicacion = models.PositiveIntegerField(verbose_name="Año de publicación")
   
    imagen_url = models.URLField(blank=True, null=True) 
    
    def __str__(self):
        return self.titulo

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'libro')
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return f"{self.libro.titulo} marcado como favorito por {self.usuario.username}"
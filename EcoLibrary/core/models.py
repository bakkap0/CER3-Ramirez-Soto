from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripción breve")
    categoria = models.CharField(max_length=100)
    anio_publicacion = models.PositiveIntegerField(verbose_name="Año de publicación")
    
   
    imagen_url = models.URLField(blank=True, null=True) 
    
    def __str__(self):
        return self.titulo
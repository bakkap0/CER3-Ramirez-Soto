from django.contrib import admin
<<<<<<< HEAD
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'fecha_publicacion')
=======
from .models import Libro, Favorito

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'anio_publicacion')
    search_fields = ('titulo', 'autor')
    list_filter = ('categoria', 'anio_publicacion')

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'fecha_agregado')
    search_fields = ('usuario__username', 'libro__titulo')
    list_filter = ('fecha_agregado',)
>>>>>>> frank/main

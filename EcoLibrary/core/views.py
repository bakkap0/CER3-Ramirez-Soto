from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
import requests 
from .models import Libro
from .serializers import LibroSerializer


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'core/lista_libros.html', {'libros': libros})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    datos_externos = {}
    
    try:
        titulo = libro.titulo.replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={titulo}"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('docs'):
                doc = data['docs'][0]
                datos_externos['puntuacion'] = doc.get('ratings_average', 'N/A')
                if 'cover_i' in doc:
                    datos_externos['portada_url'] = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"
    except Exception:
        pass 

    return render(request, 'core/detalle_libro.html', {'libro': libro, 'datos_externos': datos_externos})


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
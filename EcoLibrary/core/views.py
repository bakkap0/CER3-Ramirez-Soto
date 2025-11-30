<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Libro, Favorito
from rest_framework import viewsets, permissions
from .serializers import LibroSerializer, LibroDetalleSerializer


def obtener_datos_api_externa(titulo_o_id):
    import requests 

    API_URL = f"https://openlibrary.org/search.json?title={titulo_o_id}"
    
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status() 
        data = response.json()
        
        if data and data.get('docs'):
            first_doc = data['docs'][0]
            return {
                "portada_url_ol": f"https://covers.openlibrary.org/b/id/{first_doc.get('cover_i')}-M.jpg" if first_doc.get('cover_i') else None,
                "anio_primera_publicacion": first_doc.get('first_publish_year'),
                "nota": "Simulación de puntuación: 4.5/5"
            }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al consultar API externa: {e}"}
        
    return {"mensaje": "No se encontraron datos complementarios en la API externa."}

def registro_view(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('lista_libros')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

class LibroListView(ListView):
    model = Libro
    template_name = 'core/lista_libros.html'
    context_object_name = 'libros'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'core/detalle_libro.html'
    context_object_name = 'libro'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = self.get_object()
        context['datos_externos'] = obtener_datos_api_externa(libro.titulo) 
        user = self.request.user
        if user.is_authenticated:
            context['is_favorito'] = Favorito.objects.filter(
                usuario=user, 
                libro=libro
            ).exists()
        return context

@login_required
def marcar_favorito_view(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    favorito_qs = Favorito.objects.filter(usuario=request.user, libro=libro)
    
    if request.method == 'POST':
        if favorito_qs.exists():
            favorito_qs.delete()
        else:
            Favorito.objects.create(usuario=request.user, libro=libro) 
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('detalle_libro', kwargs={'pk': libro_id})))

@method_decorator(login_required, name='dispatch') 
class FavoritoListView(ListView):
    model = Favorito
    template_name = 'core/lista_favoritos.html' 
    context_object_name = 'favoritos'

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user).select_related('libro') 

@method_decorator(login_required, name='dispatch') 
class FavoritoDeleteView(DeleteView):
    model = Favorito
    success_url = reverse_lazy('lista_favoritos') 
    template_name = 'core/confirmar_eliminacion_favorito.html' 

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)
>>>>>>> frank/main


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
<<<<<<< HEAD
    serializer_class = LibroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
=======
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LibroDetalleSerializer
        return LibroSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny] 
        else: 
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] 
        return [permission() for permission in permission_classes]
>>>>>>> frank/main

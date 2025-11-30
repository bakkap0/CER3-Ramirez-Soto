from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/libros', views.LibroViewSet)

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('', include(router.urls)),
]
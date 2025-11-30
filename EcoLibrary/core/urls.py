from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'libros', views.LibroViewSet)

urlpatterns = [

    path('registro/', views.registro_view, name='registro'), 
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', views.LibroListView.as_view(), name='lista_libros'),
    path('libro/<int:pk>/', views.LibroDetailView.as_view(), name='detalle_libro'),
    
    path('favoritos/', views.FavoritoListView.as_view(), name='lista_favoritos'),
    path('libro/<int:libro_id>/marcar_favorito/', views.marcar_favorito_view, name='marcar_favorito'), 
    path('favorito/<int:pk>/eliminar/', views.FavoritoDeleteView.as_view(), name='eliminar_favorito'), 

    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
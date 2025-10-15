from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='index'),

    # Detalles noticias
    path('detalle/<int:pk>/', views.noticia_detalle, name='noticia_detalle'),

    # Páginas estáticas
    path('contacto/', views.contacto, name='contacto'),
    path('sobre/', views.sobre, name='sobre'),
    path('politica/', views.politica, name='politica'),

    # CRUD Categoría
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),

    # CRUD Noticia
    path('noticias/', views.noticia_lista, name='noticia_lista'),
    path('noticias/crear/', views.noticia_crear, name='noticia_crear'),
    path('noticias/<int:pk>/editar/', views.noticia_editar, name='noticia_editar'),
    path('noticias/<int:pk>/eliminar/', views.noticia_eliminar, name='noticia_eliminar'),

    # Categorías dinámicas
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),
]

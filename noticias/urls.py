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
    path('deportes/', views.deportes, name='deportes'),
    path('videos/', views.videos, name='videos'),
    path('noticias-chile/', views.chile, name='chile'),

    # CRUD Categoría
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/admin/eliminar/<int:categoria_id>/', views.confirmar_eliminar_categoria,name='confirmar_eliminar_categoria_admin'),


    # CRUD Noticia
    path('noticias/', views.noticia_lista, name='noticia_lista'),
    path('noticias/crear/', views.noticia_crear, name='noticia_crear'),
    path('noticias/<int:pk>/editar/', views.noticia_editar, name='noticia_editar'),
    path('noticias/<int:pk>/eliminar/', views.noticia_eliminar, name='noticia_eliminar'),
    path('noticia/<int:id>/', views.detalle_noticia, name='detalle_noticia'),

    # CRUD Respuestas
    path('respuestas/', views.lista_respuestas, name='lista_respuestas'),
    path('respuestas/crear/', views.crear_respuesta, name='crear_respuesta'),
    path('respuestas/crear/<int:noticia_id>/', views.crear_respuesta, name='crear_respuesta_desde_noticia'),
    path('respuestas/editar/<int:id>/', views.editar_respuesta, name='editar_respuesta'),
    path('respuestas/eliminar/<int:id>/', views.eliminar_respuesta, name='eliminar_respuesta'),

    # CRUD Reportes
    path('reportar/noticia/<int:noticia_id>/', views.reportar_noticia, name='reportar_noticia'),
    path('reportar/respuesta/<int:respuesta_id>/', views.reportar_respuesta, name='reportar_respuesta'),
    path('contacto/ajax/', views.contacto_ajax, name='contacto_ajax'),

    # Categorías dinámicas
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),

     # Registro
    path('registro/', views.registrar_usuario, name='registro'),
    path('buscar/', views.buscar, name='buscar'),

    
]

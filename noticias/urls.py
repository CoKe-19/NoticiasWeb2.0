from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # ================================
    # 🏠 Página principal
    # ================================
    path('', views.inicio, name='index'),

    # ================================
    # 📄 Páginas estáticas
    # ================================
    path('contacto/', views.contacto, name='contacto'),
    path('sobre/', views.sobre, name='sobre'),
    path('politica/', views.politica, name='politica'),
    path('deportes/', views.deportes, name='deportes'),
    path('videos/', views.videos, name='videos'),
    path('noticias-chile/', views.chile, name='chile'),
    path("autores/", views.lista_autores, name="lista_autores"),
    path('actividad/', views.actividad_reciente, name='actividad_reciente'),



    # ================================
    # 🧩 CRUD Categoría
    # ================================
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/admin/eliminar/<int:categoria_id>/', views.confirmar_eliminar_categoria, name='confirmar_eliminar_categoria_admin'),

    # ================================
    # 📰 CRUD Noticia
    # ================================
    path('noticias/', views.noticia_lista, name='noticia_lista'),
    path('noticias/crear/', views.noticia_crear, name='noticia_crear'),
    path('noticias/<int:pk>/editar/', views.noticia_editar, name='noticia_editar'),
    path('noticias/<int:pk>/eliminar/', views.noticia_eliminar, name='noticia_eliminar'),
    path('noticia/<int:id>/', views.noticia_detalle, name='noticia_detalle'),

    # ================================
    # 💬 CRUD Respuestas
    # ================================
    path('respuestas/', views.lista_respuestas, name='lista_respuestas'),
    path('respuestas/crear/', views.crear_respuesta, name='crear_respuesta'),
    path('respuestas/crear/<int:noticia_id>/', views.crear_respuesta, name='crear_respuesta_desde_noticia'),
    path('respuestas/editar/<int:id>/', views.editar_respuesta, name='editar_respuesta'),
    path('respuestas/eliminar/<int:id>/', views.eliminar_respuesta, name='eliminar_respuesta'),

    # ================================
    # 🚨 CRUD Reportes
    # ================================
    path('reportar/noticia/<int:noticia_id>/', views.reportar_noticia, name='reportar_noticia'),
    path('reportar/respuesta/<int:respuesta_id>/', views.reportar_respuesta, name='reportar_respuesta'),

    # ================================
    # 🗂️ Categorías dinámicas
    # ================================
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),

    # ================================
    # 👤 Registro y perfil de usuario
    # ================================
    path('registro/', views.registrar_usuario, name='registro'),
    path('buscar/', views.buscar, name='buscar'),
    path('contacto/', views.contacto, name='contacto'),
    path('inicio-privado/', views.inicio_privado, name='panel_privado'),
    path('mis-noticias/', views.mis_noticias, name='mis_noticias'),
    path('mis_noticias/eliminar/<int:noticia_id>/', views.confirmar_eliminar_noticia, name='noticia_confirmar_eliminar'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='ver_perfil'),

    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),

    # ================================
    # ❤️ Reacciones en noticias
    # ================================
    path('noticia/<int:noticia_id>/reaccionar/', views.reaccionar_noticia, name='reaccionar_noticia'),

    # ================================
    # ✉️ Mensajes y notificaciones
    # ================================
    path('mensajes/', views.bandeja_entrada, name='bandeja_entrada'),
    path('mensajes/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes/enviar/<str:username>/', views.enviar_a_usuario, name='enviar_a_usuario'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('feed/', views.feed, name='feed'),

    # ================================
    # 🔐 Recuperación de contraseña
    # ================================
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    # ================================
    # 🔐 Postulaciones
    # ================================
    path("postular-autor/", views.postular_autor, name="postular_autor"),
    path("panel-postulaciones/", views.panel_postulaciones, name="panel_postulaciones"),
    path("aprobar/<int:pk>/", views.aprobar_postulacion, name="aprobar_postulacion"),
    path("rechazar/<int:pk>/", views.rechazar_postulacion, name="rechazar_postulacion")
]
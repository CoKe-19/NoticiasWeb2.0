from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views_api import NoticiaViewSet, CategoriaViewSet, RespuestaViewSet, ReporteViewSet

router = DefaultRouter()
router.register("noticias", NoticiaViewSet, basename="noticia")
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("respuestas", RespuestaViewSet, basename="respuesta")
router.register("reportes", ReporteViewSet, basename="reporte")

urlpatterns = [
    path("", include(router.urls)),
]

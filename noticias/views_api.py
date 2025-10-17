from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Noticia, Categoria, Respuesta, Reporte
from .serializers import NoticiaSerializer, CategoriaSerializer, RespuestaSerializer, ReporteSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # lectura para todos, CRUD solo autenticados
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"nombre": ["exact", "icontains"]}
    search_fields = ["nombre"]
    ordering_fields = ["nombre", "id"]
    ordering = ["nombre"]


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.select_related("autor", "categoria").all()
    serializer_class = NoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "categoria": ["exact"],
        "autor": ["exact"],
        "fecha_creacion": ["gte", "lte"],
    }
    search_fields = [
        "titulo",
        "contenido",
        "autor__username",
        "categoria__nombre",
    ]
    ordering_fields = ["fecha_creacion", "id"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class RespuestaViewSet(viewsets.ModelViewSet):
    queryset = Respuesta.objects.select_related("autor", "noticia").all()
    serializer_class = RespuestaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "noticia": ["exact"],
        "autor": ["exact"],
        "fecha_creacion": ["gte", "lte"],
    }
    search_fields = ["contenido"]
    ordering_fields = ["fecha_creacion", "id"]
    ordering = ["-fecha_creacion"]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.select_related("usuario", "noticia", "respuesta").all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "noticia": ["exact"],
        "respuesta": ["exact"],
        "usuario": ["exact"],
        "fecha": ["gte", "lte"],
    }
    search_fields = ["motivo"]
    ordering_fields = ["fecha", "id"]
    ordering = ["-fecha"]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

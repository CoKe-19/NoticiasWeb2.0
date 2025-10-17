from rest_framework import serializers
from .models import Noticia, Categoria, Respuesta, Reporte

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
    
    def validate_nombre(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("El nombre de la categoría es obligatorio.")
        categoria_id = self.instance.id if self.instance else None
        if Categoria.objects.filter(nombre__iexact=value).exclude(id=categoria_id).exists():
            raise serializers.ValidationError("El nombre de la categoría ya existe.")        
        return value


class NoticiaSerializer(serializers.ModelSerializer):
    categoria_info = CategoriaSerializer(source="categoria", read_only=True)
    autor_username = serializers.CharField(source="autor.username", read_only=True)

    class Meta:
        model = Noticia
        fields = [
            "id",
            "titulo",
            "contenido",
            "categoria",
            "categoria_info",
            "autor",
            "autor_username",
            "fecha_creacion",
            "imagen",
        ]
        read_only_fields = ["fecha_creacion", "autor"]

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El título es obligatorio.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value.strip()


class RespuestaSerializer(serializers.ModelSerializer):
    autor_username = serializers.CharField(source="autor.username", read_only=True)
    noticia_titulo = serializers.CharField(source="noticia.titulo", read_only=True)

    class Meta:
        model = Respuesta
        fields = [
            "id",
            "contenido",
            "autor",
            "autor_username",
            "noticia",
            "noticia_titulo",
            "fecha_creacion",
        ]
        read_only_fields = ["fecha_creacion"]

    def validate_contenido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El contenido de la respuesta es obligatorio.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El contenido debe tener al menos 3 caracteres.")
        return value.strip()


class ReporteSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source="usuario.username", read_only=True)
    noticia_titulo = serializers.CharField(source="noticia.titulo", read_only=True)
    respuesta_contenido = serializers.CharField(source="respuesta.contenido", read_only=True)

    class Meta:
        model = Reporte
        fields = [
            "id",
            "noticia",
            "noticia_titulo",
            "respuesta",
            "respuesta_contenido",
            "usuario",
            "usuario_username",
            "motivo",
            "fecha",
        ]
        read_only_fields = ["fecha"]

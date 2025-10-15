from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='noticias')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticias')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.noticia.titulo}"

from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils import timezone
from django.contrib import admin
from django.utils.timezone import now

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

class Respuesta(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas')
    contenido = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.autor.username} en {self.noticia.titulo}"

class Reporte(models.Model):
    noticia = models.ForeignKey('Noticia', on_delete=models.CASCADE, blank=True, null=True)
    respuesta = models.ForeignKey('Respuesta', on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.TextField(max_length=500) 
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.noticia:
            return f"Reporte de {self.usuario.username} sobre noticia: {self.noticia.titulo}"
        elif self.respuesta:
            return f"Reporte de {self.usuario.username} sobre respuesta"
        return f"Reporte de {self.usuario.username}"

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_noticia_titulo', 'get_respuesta_contenido', 'motivo', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('usuario__username', 'motivo')

    def get_noticia_titulo(self, obj):
        return obj.noticia.titulo if obj.noticia else "-"
    get_noticia_titulo.short_description = "Noticia"

    def get_respuesta_contenido(self, obj):
        if obj.respuesta:
            return f"{obj.respuesta.contenido} (Titulo de la Noticia: {obj.respuesta.noticia.titulo})"
        return "-"
    get_respuesta_contenido.short_description = "Respuesta"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)
    rol = models.CharField(
        max_length=20,
        choices=[('autor', 'Autor'), ('admin', 'Administrador')],
        default='autor'
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Reaccion(models.Model):
    REACCIONES = [
        ('like', '❤️ Me gusta'),
        ('love', '😍 Me encanta'),
        ('funny', '😂 Me divierte'),
        ('wow', '😮 Me sorprende'),
        ('sad', '😢 Me entristece'),
        ('angry', '😡 Me enoja'),
    ]

    noticia = models.ForeignKey('Noticia', on_delete=models.CASCADE, related_name='reacciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=REACCIONES)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('noticia', 'usuario')
        
class Mensaje(models.Model):
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.remitente.username} ➜ {self.receptor.username}'

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    texto = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notif → {self.usuario.username}: {self.texto}"

    class Meta:
        ordering = ['-fecha']

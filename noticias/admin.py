from django.contrib import admin
from .models import Noticia, Comentario, Categoria

# Register your models here.
admin.site.register(Noticia)
admin.site.register(Categoria)
admin.site.register(Comentario)
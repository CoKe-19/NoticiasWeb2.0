from django.contrib import admin
from .models import Noticia,Respuesta,Categoria

# Register your models here.
admin.site.register(Noticia)
admin.site.register(Categoria)
admin.site.register(Respuesta)


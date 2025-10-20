from .models import Notificacion

def crear_notificacion(usuario, texto, url=""):
    Notificacion.objects.create(usuario=usuario, texto=texto, url=url)

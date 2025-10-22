from .models import Notificacion


def crear_notificacion(usuario, tipo, contenido, url=None):
    """Crea una notificación genérica para un usuario"""
    Notificacion.objects.create(
        usuario=usuario,
        tipo=tipo,
        contenido=contenido,
        url=url
    )

from .models import Notificacion, Mensaje

def contadores_globales(request):
    """Agrega contadores globales de notificaciones y mensajes a todas las plantillas."""
    if request.user.is_authenticated:
        notif_count = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        mensajes_no_leidos = Mensaje.objects.filter(receptor=request.user, leido=False).count() if hasattr(request.user, 'mensaje_set') else 0
    else:
        notif_count = 0
        mensajes_no_leidos = 0

    return {
        'notif_count': notif_count,
        'mensajes_no_leidos': mensajes_no_leidos,
    }

def notificaciones_context(request):
    if request.user.is_authenticated:
        notif_count = Notificacion.objects.filter(usuario=request.user, leido=False).count()
    else:
        notif_count = 0
    return {'notif_count': notif_count}
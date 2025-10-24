from django.utils import timezone

class ActualizarUltimaActividadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, "perfil"):
            perfil = request.user.perfil
            perfil.ultima_actividad = timezone.now()
            perfil.save(update_fields=["ultima_actividad"])
        response = self.get_response(request)
        return response

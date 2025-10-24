from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.db.models import ProtectedError
from django.urls import reverse
from .models import Noticia, Categoria, Respuesta, Reporte , Reaccion , Mensaje ,Notificacion , Actividad ,PostulacionAutor
from .utils import crear_notificacion
from django.core.paginator import Paginator
from django.contrib.auth.models import Group

from .forms import (
    NoticiaForm, CategoriaForm, RespuestaForm, ReporteForm, RegistroForm, ContactoForm, CustomAuthenticationForm , PerfilForm , MensajeForm
)

User = get_user_model()


# ===========================
# Noticias
# ===========================
def inicio(request):
    noticias_destacadas = Noticia.objects.order_by('-fecha_creacion')[:3]
    ultimas_noticias = Noticia.objects.order_by('-fecha_creacion')[:6]
    return render(request, 'noticias/index.html', {
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias
    })

def noticia_lista(request):
    noticias = Noticia.objects.all().order_by('-fecha_creacion')
    return render(request, 'noticias/noticia_lista.html', {'noticias': noticias})

@login_required
def noticia_crear(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            messages.success(request, '¡Noticia creada correctamente!')
            return redirect('noticia_lista')
        else:
            messages.error(request, 'Hubo un error al crear la noticia.')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Crear Noticia',
        'boton_texto': 'Crear',
        'cancelar_url': '/noticias/'  
    })

@login_required
def noticia_editar(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.user != noticia.autor:
        messages.error(request, 'No tienes permiso para editar esta noticia.')
        return redirect('noticia_lista')
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Noticia editada correctamente!')
            return redirect('noticia_detalle', pk=pk)
        else:
            messages.error(request, 'Hubo un error al editar la noticia.')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Editar Noticia',
        'boton_texto': 'Guardar cambios',
        'cancelar_url': reverse('noticia_detalle', args=[pk])
    })


# ==========================
# Actividades
# ==========================

def registrar_actividad(usuario, accion, url=""):
    Actividad.objects.create(usuario=usuario, accion=accion, url=url)

def actividad_reciente(request):
    actividades = Actividad.objects.order_by('-fecha')[:5]
    return render(request, 'noticias/actividad.html', {'actividades': actividades})

@login_required
def noticia_detalle(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    respuestas = Respuesta.objects.filter(noticia=noticia).order_by('fecha_creacion')

    conteos = {
        'like': noticia.reacciones.filter(tipo='like').count(),
        'love': noticia.reacciones.filter(tipo='love').count(),
        'funny': noticia.reacciones.filter(tipo='funny').count(),
        'wow': noticia.reacciones.filter(tipo='wow').count(),
        'sad': noticia.reacciones.filter(tipo='sad').count(),
        'angry': noticia.reacciones.filter(tipo='angry').count(),
    }

    reaccion_usuario = None
    if request.user.is_authenticated:
        reaccion = Reaccion.objects.filter(noticia=noticia, usuario=request.user).first()
        if reaccion:
            reaccion_usuario = reaccion.tipo

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            nueva_respuesta = form.save(commit=False)
            nueva_respuesta.noticia = noticia
            nueva_respuesta.autor = request.user
            nueva_respuesta.save()
            if noticia.autor != request.user:
                crear_notificacion(
                    usuario=noticia.autor,
                    tipo="comentario",
                    contenido=f"💬 {request.user.username} comentó tu noticia: {noticia.titulo}",
                    url=reverse('noticia_detalle', args=[noticia.id])
                )
            registrar_actividad(
                usuario=request.user,
                accion=f"comentó en “{noticia.titulo}”",
                url=reverse('noticia_detalle', args=[noticia.id])
            )

            return redirect('noticia_detalle', id=noticia.id)
    else:
        form = RespuestaForm()

    context = {
        'noticia': noticia,
        'respuestas': respuestas,
        'conteos': conteos,
        'reaccion_usuario': reaccion_usuario,
        'form': form,
    }
    return render(request, 'noticias/noticia_detalle.html', context)


@login_required(login_url="login")
def noticia_eliminar(request, pk): 
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.user != noticia.autor and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar esta noticia.", status=403)
    if request.method == "POST":
        noticia.delete()
        messages.success(request, "Noticia eliminada correctamente.")
        if request.user.is_staff:
            return redirect('noticia_lista') 
        else:
            return redirect('mis_noticias')  
    if request.user.is_staff:
        cancelar_url = reverse('noticia_lista')
    else:
        cancelar_url = reverse('mis_noticias')
    return render(request, 'noticias/confirm_delete.html', {
        'objeto': noticia,
        'tipo': 'Noticia',
        'cancelar_url': cancelar_url
    })

@login_required
def mis_noticias(request):
    noticias = Noticia.objects.filter(autor=request.user).order_by('-fecha_creacion')
    if request.method == "POST":
        noticia_id = request.POST.get("noticia_id")
        action = request.POST.get("action")
        noticia = get_object_or_404(Noticia, id=noticia_id, autor=request.user)
        if action == "eliminar":
            noticia.delete()
            messages.success(request, f'La noticia "{noticia.titulo}" fue eliminada correctamente.')
            return redirect('mis_noticias')
        elif action == "editar":
            messages.info(request, f'La noticia "{noticia.titulo}" se puede editar en el panel de administración.')
            return redirect('mis_noticias')
    return render(request, 'noticias/mis_noticias.html', {'noticias': noticias})

@login_required
def confirmar_eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id, autor=request.user)
    cancelar_url = request.META.get('HTTP_REFERER', reverse('mis_noticias'))
    if request.method == "POST":
        noticia.delete()
        messages.success(request, f'La noticia "{noticia.titulo}" fue eliminada correctamente.')
        return redirect('mis_noticias')
    return render(request, 'noticias/confirm_delete.html', {
        'objeto': noticia,
        'tipo': 'Noticia',
        'cancelar_url': cancelar_url
    })

# ===========================
# Categorías
# ===========================
def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    noticias = Noticia.objects.filter(categoria=categoria)
    return render(request, 'noticias/categoria_lista.html', {
        'categoria': categoria,
        'noticias': noticias
    })

@login_required
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría creada correctamente!')
            return redirect('categoria_lista')
        else:
            messages.error(request, 'Hubo un error al crear la categoría.')
    else:
        form = CategoriaForm()
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Crear Categoría',
        'boton_texto': 'Crear',
        'cancelar_url': '/categorias/'
    })

@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría editada correctamente!')
            return redirect('categoria_lista')
        else:
            messages.error(request, 'Hubo un error al editar la categoría.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Editar Categoría',
        'boton_texto': 'Guardar cambios',
        'cancelar_url': reverse('categoria_lista')
    })

@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if categoria.noticias.exists():
        messages.error(request, 'No se puede eliminar esta categoría porque tiene noticias asociadas.')
        return redirect('categoria_lista')
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, '¡Categoría eliminada correctamente!')
        return redirect('categoria_lista')
    return render(request, 'noticias/confirm_delete.html', {
        'objeto': categoria,
        'cancelar_url': '/categorias/'
    })

@login_required(login_url="login")
def confirmar_eliminar_categoria(request, categoria_id):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso.", status=403)
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if categoria.noticias.exists():
        messages.error(request, "No se puede eliminar la categoría porque tiene noticias asociadas.")
        return redirect('categoria_lista')
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('categoria_lista')
    return render(request, 'noticias/categoria_confirm_delete.html', {
        'objeto': categoria,
        'tipo': 'Categoría',
        'cancelar_url': reverse('categoria_lista')
    })

# ===========================
# Respuestas
# ===========================
@login_required
def crear_respuesta(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.autor = request.user
            respuesta.noticia = noticia
            respuesta.save()
            messages.success(request, '¡Comentario creado correctamente!')
            return redirect('detalle_noticia', id=noticia.id)
        else:
            messages.error(request, 'Hubo un error al crear el comentario.')
    else:
        form = RespuestaForm()
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Agregar Respuesta',
        'boton_texto': 'Publicar',
        'cancelar_url': f'/noticia/{noticia.id}/'
    })

@login_required
def editar_respuesta(request, id):
    respuesta = get_object_or_404(Respuesta, id=id)
    noticia = respuesta.noticia
    if request.user != respuesta.autor and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para editar este comentario.')
        return redirect('noticia_detalle', id=noticia.id)
    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Comentario editado correctamente!')
            return redirect('noticia_detalle', id=noticia.id)
        else:
            messages.error(request, 'Hubo un error al editar el comentario.')
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Editar Respuesta',
        'boton_texto': 'Guardar cambios',
        'cancelar_url': reverse('noticia_detalle', args=[noticia.id])
    })

@login_required(login_url="login")
def eliminar_respuesta(request, id):
    respuesta = get_object_or_404(Respuesta, id=id)
    if request.user != respuesta.autor and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar esta respuesta.", status=403)
    if request.method == "POST":
        respuesta.delete()
        messages.success(request, "Respuesta eliminada correctamente.")
        return redirect('noticia_detalle', id=respuesta.noticia.id)
    cancelar_url = reverse('noticia_detalle', kwargs={'id': respuesta.noticia.id})
    return render(request, 'noticias/confirm_delete.html', {
        'objeto': respuesta,
        'tipo': 'Respuesta',
        'cancelar_url': cancelar_url
    })

def lista_respuestas(request):
    respuestas = Respuesta.objects.select_related('noticia').order_by('-fecha_creacion')
    return render(request, 'noticias/respuestas_list.html', {'respuestas': respuestas})

# ===========================
# Reportes
# ===========================
@login_required
def reportar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    tipo_objetivo = "Noticia"  
    if request.method == "POST":
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.noticia = noticia
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, '¡Reporte enviado correctamente!')
            return redirect('noticia_detalle', id=noticia.id)
        else:
            messages.error(request, 'Hubo un error al enviar el reporte.')
    else:
        form = ReporteForm()
    return render(request, 'noticias/reporte_form.html', {
        'form': form,
        'objetivo': noticia,
        'tipo_objetivo': tipo_objetivo
    })

@login_required
def reportar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    tipo_objetivo = "Respuesta"
    if request.method == "POST":
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.respuesta = respuesta
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, '¡Reporte enviado correctamente!')
            return redirect('noticia_detalle', id=respuesta.noticia.id)
        else:
            messages.error(request, 'Hubo un error al enviar el reporte.')
    else:
        form = ReporteForm()
    return render(request, 'noticias/reporte_form.html', {
        'form': form,
        'objetivo': respuesta,
        'tipo_objetivo': tipo_objetivo
    })

# ===========================
# Autenticación / Usuarios
# ===========================
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta fue creada con éxito! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

# ===========================
# Contacto
# ===========================
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            messages.success(request, '✅ ¡Tu mensaje ha sido enviado correctamente!')
            return redirect('contacto')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = ContactoForm()

    return render(request, 'noticias/contacto.html', {'form': form})

    
@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'noticias/categoria_lista.html', {'categorias': categorias})

def buscar(request):
    query = request.GET.get('q', '').strip()
    resultados = []

    if query:
        resultados = Noticia.objects.filter(titulo__icontains=query)[:6]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'noticias/resultados_ajax.html', {'resultados': resultados})

    return render(request, 'noticias/buscar.html', {'resultados': resultados, 'query': query})


def perfil_usuario(request, username):
    user = get_object_or_404(User, username=username)
    noticias = Noticia.objects.filter(autor=user)
    return render(request, 'noticias/perfil.html', {
        'perfil': user.perfil,
        'noticias': noticias,
    })
    

@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Perfil actualizado correctamente.")
            return redirect('ver_perfil', username=request.user.username)
        else:
            messages.error(request, "❌ Hubo un error al actualizar el perfil.")
    else:
        form = PerfilForm(instance=perfil, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'noticias/editar_perfil.html', {'form': form})
    
@login_required
def reaccionar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    tipo = request.POST.get('tipo')

    if not tipo:
        return JsonResponse({'success': False, 'error': 'Tipo de reacción no válido'})

    reaccion = Reaccion.objects.filter(noticia=noticia, usuario=request.user).first()

    if reaccion and reaccion.tipo == tipo:
        reaccion.delete()
        accion = 'removed'
    else:
        Reaccion.objects.update_or_create(
            noticia=noticia,
            usuario=request.user,
            defaults={'tipo': tipo}
        )
        accion = 'added'

    conteos = {
        'like': noticia.reacciones.filter(tipo='like').count(),
        'love': noticia.reacciones.filter(tipo='love').count(),
        'funny': noticia.reacciones.filter(tipo='funny').count(),
        'wow': noticia.reacciones.filter(tipo='wow').count(),
        'sad': noticia.reacciones.filter(tipo='sad').count(),
        'angry': noticia.reacciones.filter(tipo='angry').count(),
    }

    return JsonResponse({'success': True, 'accion': accion, 'counts': conteos})

@login_required
def enviar_mensaje(request):
    para_username = request.GET.get('para')
    receptor = None
    if para_username:
        receptor = get_object_or_404(User, username=para_username)
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if receptor:
            form.data = form.data.copy()
            form.data['receptor'] = receptor.id
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            crear_notificacion(
                usuario=mensaje.receptor,
                tipo="mensaje",
                contenido=f"📩 Nuevo mensaje de {request.user.username}",
                url=reverse('bandeja_entrada')
            )
            messages.success(request, f"Mensaje enviado correctamente a {mensaje.receptor.username}")
            return redirect('bandeja_entrada')
        else:
            messages.error(request, "Hubo un error al enviar el mensaje")
    else:
        form = MensajeForm(initial={'receptor': receptor})
    return render(request, 'noticias/enviar.html', {'form': form, 'receptor': receptor})



@login_required
def bandeja_entrada(request):
    mensajes = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')
    return render(request, 'noticias/entrada.html', {'mensajes': mensajes})


@login_required
def notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    notificaciones.update(leido=True)
    return render(request, 'noticias/notificaciones.html', {'notificaciones': notificaciones})


@login_required
def feed(request):
    noticias = Noticia.objects.all().select_related('autor').prefetch_related('reacciones').order_by('-fecha_creacion')
    for n in noticias:
        n.likes = n.reacciones.filter(tipo='like').count()
        n.wows = n.reacciones.filter(tipo='wow').count()
        try:
            if hasattr(n, 'respuestas'):
                n.respuestas_count = n.respuestas.count()
            else:
                n.respuestas_count = n.respuesta_set.count()
        except Exception:
            n.respuestas_count = 0
        n.respuestas_count = n.respuestas_count or 0
        n.likes = n.likes or 0
        n.wows = n.wows or 0

    return render(request, 'noticias/feed.html', {'noticias': noticias})

def reporteros(request):
    qs = User.objects.select_related('perfil').all().order_by('username')
    paginator = Paginator(qs, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "noticias/reporteros.html", {
        "reporteros": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    })

def sobre(request):
    return render(request, 'noticias/sobre.html')

def deportes(request):
    return render(request,'noticias/deportes.html')

def videos(request):
    return render(request,'noticias/videos.html')

def chile(request):
    return render(request,'noticias/noticia_chile.html')

def politica(request):
    return render(request, 'noticias/politica.html')


@login_required
def inicio_privado(request):
    total_noticias = Noticia.objects.count()
    total_colaboradores = User.objects.filter(
        noticias__isnull=False,
        is_superuser=False
    ).distinct().count()
    total_comentarios = Respuesta.objects.count()
    total_reportes = Reporte.objects.count()
    actividades = Actividad.objects.order_by('-fecha')[:5]

    context = {
        'total_noticias': total_noticias,
        'total_colaboradores': total_colaboradores,
        'total_comentarios': total_comentarios,
        'total_reportes': total_reportes,
        'actividades': actividades,
    }
    return render(request, 'noticias/panel_privado.html', context)

@login_required
def postular_autor(request):
    if PostulacionAutor.objects.filter(usuario=request.user).exists():
        messages.warning(request, "⚠️ Ya has enviado una postulación. Espera la respuesta antes de volver a postular.")
        return redirect("index")
    if request.method == "POST":
        experiencia = request.POST.get("experiencia")
        motivo = request.POST.get("motivo")
        correo_contacto = request.POST.get("correo_contacto")
        PostulacionAutor.objects.create(
            usuario=request.user,
            experiencia=experiencia,
            motivo=motivo,
            correo_contacto=correo_contacto,
        )

        messages.success(request, "✅ Tu postulación fue enviada correctamente. Te contactaremos pronto.")
        return redirect("index")
    return render(request, "noticias/postular_autor.html")

@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_postulaciones(request):
    postulaciones = PostulacionAutor.objects.all().order_by("-fecha")
    return render(request, "noticias/panel_postulaciones.html", {"postulaciones": postulaciones})


@login_required
@user_passes_test(lambda u: u.is_staff)
def aprobar_postulacion(request, pk):
    postulacion = get_object_or_404(PostulacionAutor, pk=pk)
    postulacion.aprobada = True
    postulacion.revisada = True
    postulacion.save()
    user = postulacion.usuario
    user.is_staff = True
    autores_group, created = Group.objects.get_or_create(name="Autores")
    user.groups.add(autores_group)
    user.save()
    messages.success(request, f"✅ {user.username} fue aprobado como Autor.")
    return redirect("panel_postulaciones")

@login_required
@user_passes_test(lambda u: u.is_staff)
def rechazar_postulacion(request, pk):
    postulacion = get_object_or_404(PostulacionAutor, pk=pk)
    postulacion.revisada = True
    postulacion.aprobada = False
    postulacion.save()
    messages.error(request, f"❌ Postulación de {postulacion.usuario.username} rechazada.")
    return redirect("panel_postulaciones")

def lista_autores(request):
    autores_aprobados = User.objects.filter(postulacionautor__aprobada=True)
    admins = User.objects.filter(is_staff=True)
    reporteros = (autores_aprobados | admins).distinct()
    context = {"reporteros": reporteros}
    return render(request, "noticias/autores.html", context)
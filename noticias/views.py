from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria , Respuesta ,Reporte
from .forms import NoticiaForm, CategoriaForm ,RespuestaForm , ReporteForm , RegistroForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse

def inicio(request):
    noticias_destacadas = Noticia.objects.order_by('-fecha_creacion')[:3]
    ultimas_noticias = Noticia.objects.order_by('-fecha_creacion')[:6]
    return render(request, 'noticias/index.html', {
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias
    })

def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    noticias = Noticia.objects.filter(categoria=categoria)
    return render(request, 'noticias/categoria.html', {
        'categoria': categoria,
        'noticias': noticias
    })

def politica(request):
    return render(request, 'noticias/politica.html')

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, 'noticias/noticia_detalle.html', {'noticia': noticia})

def contacto(request):
    return render(request, 'noticias/contacto.html')

def sobre(request):
    return render(request, 'noticias/sobre.html')

def deportes(request):
    return render(request,'noticias/deportes.html')

def videos(request):
    return render(request,'noticias/videos.html')

def chile(request):
    return render(request,'noticias/noticia_chile.html')


@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'noticias/categoria_lista.html', {'categorias': categorias})

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

def noticia_lista(request):
    noticias = Noticia.objects.all().order_by('-fecha_creacion')
    return render(request, 'noticias/noticia_lista.html', {'noticias': noticias})

def noticia_detalle(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    respuestas = noticia.respuestas.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.noticia = noticia
            respuesta.autor = request.user
            respuesta.save()
            return redirect('noticia_detalle', pk=pk)
    else:
        form = RespuestaForm()
    return render(request, 'noticias/noticia_detalle.html', {'noticia': noticia, 'respuestas': respuestas, 'form': form})

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

@login_required(login_url="login")
def noticia_eliminar(request, pk):
    noticia = get_object_or_404(Noticia, id=pk)

    if request.user != noticia.autor and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar esta noticia.", status=403)

    if request.method == "POST":
        noticia.delete()
        messages.success(request, "Noticia eliminada correctamente.")
        return redirect('noticia_lista')  # o la URL que corresponda

    return render(request, 'noticias/confirm_delete.html', {
        'objeto': noticia,
        'tipo': 'Noticia',
        'cancelar_url': f"/noticias/{noticia.id}/"  # o donde quieras que redirija si cancela
    })
def contacto(request):
    enviado = False

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        enviado = True

    return render(request, 'noticias/contacto.html', {'enviado': enviado})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

def lista_respuestas(request):
    respuestas = Respuesta.objects.select_related('noticia').order_by('-fecha_creacion')
    return render(request, 'noticias/respuestas_list.html', {'respuestas': respuestas})

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
        return redirect('detalle_noticia', id=noticia.id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Comentario editado correctamente!')
            return redirect('detalle_noticia', id=noticia.id)
        else:
            messages.error(request, 'Hubo un error al editar el comentario.')
    else:
        form = RespuestaForm(instance=respuesta)
    
    return render(request, 'noticias/form.html', {
        'form': form,
        'titulo': 'Editar Respuesta',
        'boton_texto': 'Guardar cambios',
        'cancelar_url': reverse('detalle_noticia', args=[noticia.id])
    })

@login_required(login_url="login")
def eliminar_respuesta(request, id):
    respuesta = get_object_or_404(Respuesta, id=id)

    if request.user != respuesta.autor and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar esta respuesta.", status=403)

    if request.method == "POST":
        respuesta.delete()
        messages.success(request, "Respuesta eliminada correctamente.")
        return redirect('detalle_noticia', id=respuesta.noticia.id)

    return render(request, 'noticias/confirm_delete.html', {
        'objeto': respuesta,
        'tipo': 'Respuesta',
        'cancelar_url': f"/noticias/{respuesta.noticia.id}/"
    })

def detalle_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    respuestas = noticia.respuestas.all().order_by('-fecha_creacion')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = RespuestaForm(request.POST)
            if form.is_valid():
                respuesta = form.save(commit=False)
                respuesta.noticia = noticia
                respuesta.autor = request.user
                respuesta.save()
                return redirect('detalle_noticia', id=noticia.id)
        else:
            return redirect('login')
    else:
        form = RespuestaForm()

    return render(request, 'noticias/noticia_detalle.html', {
        'noticia': noticia,
        'respuestas': respuestas,
        'form': form,
    })

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
            return redirect('detalle_noticia', id=noticia.id)
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
            return redirect('detalle_noticia', id=respuesta.noticia.id)
        else:
            messages.error(request, 'Hubo un error al enviar el reporte.')
    else:
        form = ReporteForm()
    return render(request, 'noticias/reporte_form.html', {
        'form': form,
        'objetivo': respuesta,
        'tipo_objetivo': tipo_objetivo
    })

@csrf_protect
def contacto_ajax(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': '¡Mensaje enviado correctamente!'})
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

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


@login_required(login_url="login")
def confirmar_eliminar_categoria(request, categoria_id):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso.", status=403)

    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Verificar si hay noticias asociadas usando el related_name correcto
    if categoria.noticias.exists():  
        messages.error(request, "No se puede eliminar la categoría porque tiene noticias asociadas.")
        return redirect('categoria_lista')

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('categoria_lista')

    return render(request, 'noticias/categoria_confirm_delete.html', {'categoria': categoria})

def buscar(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = Noticia.objects.filter(titulo__icontains=query)
    return render(request, 'noticias/buscar.html', {
        'query': query,
        'resultados': resultados
    })
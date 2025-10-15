from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Noticia, Comentario, Categoria
from .forms import NoticiaForm, ComentarioForm, CategoriaForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


def inicio(request):
    noticias_destacadas = Noticia.objects.order_by('-fecha_creacion')[:3]
    ultimas_noticias = Noticia.objects.order_by('-fecha_creacion')[:6]
    return render(request, 'noticias/index.html', {
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias
    })

# Página por categoría
def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    noticias = Noticia.objects.filter(categoria=categoria)
    return render(request, 'noticias/categoria.html', {
        'categoria': categoria,
        'noticias': noticias
    })


def politica(request):
    return render(request, 'noticias/politica.html')


# Detalle de una noticia
def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    return render(request, 'noticias/detalle_noticia.html', {'noticia': noticia})

# Contacto
def contacto(request):
    return render(request, 'noticias/contacto.html')

# Sobre nosotros
def sobre(request):
    return render(request, 'noticias/sobre.html')

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
            return redirect('categoria_lista')
    else:
        form = CategoriaForm()
    return render(request, 'noticias/categoria_form.html', {'form': form})

@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'noticias/categoria_form.html', {'form': form})

@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_lista')
    return render(request, 'noticias/categoria_confirm_delete.html', {'categoria': categoria})

def noticia_lista(request):
    noticias = Noticia.objects.all().order_by('-fecha_creacion')
    return render(request, 'noticias/noticia_lista.html', {'noticias': noticias})

def noticia_detalle(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    comentarios = noticia.comentarios.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = noticia
            comentario.autor = request.user
            comentario.save()
            return redirect('noticia_detalle', pk=pk)
    else:
        form = ComentarioForm()
    return render(request, 'noticias/noticia_detalle.html', {'noticia': noticia, 'comentarios': comentarios, 'form': form})

@login_required
def noticia_crear(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect('noticia_lista')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/noticia_form.html', {'form': form})

@login_required
def noticia_editar(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.user != noticia.autor:
        return redirect('noticia_lista')
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticia_detalle', pk=pk)
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticias/noticia_form.html', {'form': form})

@login_required
def noticia_eliminar(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.user != noticia.autor:
        return redirect('noticia_lista')
    if request.method == 'POST':
        noticia.delete()
        return redirect('noticia_lista')
    return render(request, 'noticias/noticia_confirm_delete.html', {'noticia': noticia})

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
from django import forms
from .models import Noticia, Comentario, Categoria
from django.contrib.auth.forms import AuthenticationForm

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'})
        }

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'categoria', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la noticia'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenido de la noticia', 'rows': 5}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario', 'rows': 3}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )
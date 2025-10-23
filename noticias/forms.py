from django import forms
from .models import Noticia,Categoria ,Respuesta ,Reporte , Perfil , Mensaje
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class RespuestaForm(forms.ModelForm):
    contenido = forms.CharField(
        label="Tu respuesta",
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu respuesta aquí...',
            'rows': 4,
            'class': 'form-control rounded-3 shadow-sm'
        })
    )

    class Meta:
        model = Respuesta
        fields = ['contenido']

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

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el motivo del reporte...'
            }),
        }


class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        help_text="",  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre de usuario'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        help_text="", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crea una contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        help_text="", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Tu nombre completo'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    asunto = forms.CharField(
        label="Asunto",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Motivo del mensaje'
        })
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...'
        })
    )

    
class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        label="Apellido",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tuemail@ejemplo.com'})
    )

    class Meta:
        model = Perfil
        fields = ['avatar', 'banner', 'bio', 'twitter', 'github', 'instagram', 'linkedin', 'sitio_web']
        labels = {
            'avatar': 'Foto de perfil',
            'banner': 'Banner de portada',
            'bio': 'Biografía',
            'twitter': 'Twitter',
            'github': 'GitHub',
            'instagram': 'Instagram',
            'linkedin': 'LinkedIn',
            'sitio_web': 'Sitio web personal',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos algo sobre ti...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/usuario'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/usuario'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/usuario'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/usuario'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://tusitio.com'}),
        }

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.user
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)
        if commit:
            user.save()
            perfil.save()
        return perfil


class MensajeForm(forms.ModelForm):
    receptor = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label='Enviar a',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    contenido = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Escribe tu mensaje...'
        })
    )

    class Meta:
        model = Mensaje
        fields = ['receptor', 'contenido']
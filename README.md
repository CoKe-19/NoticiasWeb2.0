# WebNoticias

**WebNoticias** es una plataforma web desarrollada con Django y Django REST Framework, que permite publicar, comentar, reaccionar y reportar noticias. También incluye funcionalidades de autenticación, mensajería privada y una API RESTful. Creada por : (CoKe)

---

## 🚀 Funcionalidades principales

- ✅ Registro e inicio de sesión de usuarios.
- 📰 CRUD de Noticias con imágenes y categorías.
- 💬 Respuestas (comentarios) a noticias.
- ❤️ Reacciones tipo "me gusta", "me encanta", "me sorprende", etc.
- 🚨 Reporte de noticias y comentarios.
- 📬 Sistema de mensajes privados entre usuarios.
- 🔍 Buscador Ajax de noticias.
- 👤 Perfiles de usuario con avatar.
- 🌐 API REST para Noticias, Categorías, Comentarios y Reportes.
- 🔐 Seguridad con JWT y Token Auth.
- 🛡️ Rate Limiting para APIs.
- 📦 Paginación, filtros y ordenamiento para API.

---

## 🧰 Tecnologías utilizadas

- Python 3.11+
- Django 5.2.5
- Django REST Framework
- JWT + Token Authentication
- Bootstrap 5 + CSS personalizado
- SQLite (por defecto)
- CORS Headers
- Django Filters
- DRF Spectacular (documentación OpenAPI)

---

## ⚙️ Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/webnoticias.git
cd webnoticias
```

2. Crea un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecuta las migraciones:

```bash
python manage.py migrate
```

5. Crea un superusuario:

```bash
python manage.py createsuperuser
```

6. Inicia el servidor:

```bash
python manage.py runserver
```

---

## 🔐 Autenticación API

Se incluyen 3 tipos de autenticación para el uso de la API:

- Token Auth: `Token <token>`
- JWT: `Bearer <access_token>`
- Session (para el admin o desarrollo)

La documentación OpenAPI está disponible en: `http://localhost:8000/api/schema/swagger-ui/`

---

## 📝 Estructura del proyecto

- `noticias/models.py`: Modelos principales (Noticia, Respuesta, Reporte, etc.)
- `noticias/views.py`: Vistas para interfaz web (HTML)
- `noticias/views_api.py`: Vistas API REST (DRF ViewSets)
- `noticias/forms.py`: Formularios personalizados
- `noticias/serializers.py`: Serializadores DRF
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JS, imágenes)

---

## 📂 Licencia

MIT - 2025

---

## ✨ Autor

Desarrollado por **Jorge ** 
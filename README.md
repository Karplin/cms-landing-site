# CMS de sitio institucional

Sitio público de varias páginas y panel de administración en `/admin`, con el
contenido en base de datos. Flask + PostgreSQL, todo en contenedores.

![Flask](https://img.shields.io/badge/Flask-3.x-000000) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## Puesta en marcha con Docker

```bash
cp .env.example .env      # y edita las contraseñas
docker compose up -d --build
```

| | Dirección |
|---|---|
| Sitio | http://localhost:5050 |
| Panel | http://localhost:5050/admin |
| PostgreSQL | `localhost:5433` |

El primer arranque crea el esquema, siembra el contenido de ejemplo y da de alta
el usuario indicado en `CMS_ADMIN_USER` / `CMS_ADMIN_PASSWORD`. Entra al panel y
cámbiale la contraseña.

Comandos útiles:

```bash
docker compose logs -f web
```

```bash
docker compose down
```

Para empezar de cero, incluyendo los datos:

```bash
docker compose down -v
```

## Sin Docker (desarrollo local)

Si no hay `DATABASE_URL`, la aplicación usa un archivo SQLite (`cms.db`) y no
necesita ningún servicio aparte:

```bash
pip install -r requirements.txt && python app.py
```

Queda en http://127.0.0.1:5000. Es el mismo código: solo cambia el motor.

## Variables de entorno

| Variable | Para qué sirve |
|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL. Si falta, se usa SQLite. |
| `POSTGRES_USER` · `POSTGRES_PASSWORD` · `POSTGRES_DB` | Credenciales del contenedor de base de datos. |
| `DB_PORT` | Puerto de PostgreSQL en la máquina anfitriona (5433 por defecto). |
| `WEB_PORT` | Puerto del sitio en la máquina anfitriona (5050 por defecto). |
| `CMS_SECRET_KEY` | Clave de firma de sesiones. Si falta, se genera y se guarda en la base. |
| `CMS_ADMIN_USER` · `CMS_ADMIN_PASSWORD` | Usuario inicial. Solo se usan cuando no hay ninguno. |
| `CMS_COOKIE_SECURE` | Ponla a `1` detrás de HTTPS para que la cookie solo viaje cifrada. |
| `CMS_DB_PATH` | Ruta del archivo SQLite en desarrollo local. |

## Páginas

| Ruta | Contenido |
|---|---|
| `/` | Portada: hero con slider y un resumen de cada sección |
| `/quienes-somos` | Áreas de trabajo y contadores |
| `/programas` | Todos los proyectos |
| `/noticias` | Noticias y eventos |
| `/territorio` | Voces de las sedes |
| `/documentacion` | Boletines y memorias |

El menú se define en la lista `NAV` de `app.py`: cada entrada es un endpoint y
su etiqueta.

## Qué se gestiona desde el panel

**Contenido** — registros que se repiten. Cada uno se ordena con las flechas, se
oculta sin borrarlo y se elimina:

- Diapositivas del hero
- Áreas de trabajo
- Voces del territorio
- Contadores
- Proyectos
- Noticias y Eventos
- Documentación (boletines y memorias)
- Enlaces del pie y enlaces legales

**Encabezados de sección** — el antetítulo, el título y la bajada que abren cada
bloque. Son también los que titulan las páginas interiores.

**Ajustes generales** — identidad, cabecera, columnas del pie, dirección, redes,
copyright y aviso de cookies.

**Usuarios** — alta, edición, activación y baja. Las contraseñas se guardan
cifradas (PBKDF2 vía Werkzeug); nunca se almacenan en claro. Nadie puede
eliminar ni desactivar su propia cuenta, y siempre queda al menos un usuario
activo.

## Modo claro y oscuro

El sitio abre en claro. El botón de la cabecera cambia a oscuro y la elección se
recuerda en `localStorage`. La paleta entera son variables CSS al inicio de
`static/css/site.css`: `:root` define el modo claro y `:root[data-theme="dark"]`
el oscuro.

## Estructura

```
.
├── app.py              Rutas públicas, panel, sesión y usuarios
├── db.py               PostgreSQL o SQLite tras la misma interfaz
├── schema.py           Definición del contenido: de aquí salen tablas y formularios
├── seed_data.py        Contenido inicial
├── docker-compose.yml  Base de datos + aplicación
├── Dockerfile          Imagen de la aplicación (gunicorn)
├── templates/
│   ├── base.html       Cabecera, pie y aviso de cookies
│   ├── _macros.html    Tarjetas y bloques compartidos
│   ├── index.html      Portada
│   ├── quienes_somos.html · programas.html · noticias.html
│   ├── territorio.html · documentacion.html
│   └── admin/          Panel
└── static/
    ├── css/site.css    Estilos del sitio
    ├── css/admin.css   Estilos del panel
    └── js/site.js      Slider, menú móvil, tema y aviso de cookies
```

## Añadir un campo nuevo

Todo el panel se genera desde `schema.py`. Para añadir, por ejemplo, un
subtítulo a los proyectos:

1. Añade el campo a `CONTENT_TYPES["projects"]["fields"]`.
2. Recrea la tabla (`docker compose down -v`) o añade la columna con `ALTER TABLE`.
3. Úsalo en `templates/index.html` o en la página que corresponda.

El formulario, el listado y la columna de la tabla aparecen solos.

## Notas para producción

- Cambia todas las contraseñas del `.env` y define `CMS_SECRET_KEY`.
- Sirve detrás de HTTPS con `CMS_COOKIE_SECURE=1`.
- No publiques el puerto de PostgreSQL fuera de la red de Docker.
- Pendiente si el panel queda expuesto a internet: **tokens CSRF** en los
  formularios del panel y **límite de intentos** en el login. Hoy la protección
  es la cookie de sesión con `SameSite=Lax`.

# -*- coding: utf-8 -*-
"""CMS del Instituto de Cooperación Regional.

Portada pública renderizada desde SQLite y panel de administración en /admin.
Arranque:  python app.py   ->  http://127.0.0.1:5000
"""

import os
import re
import secrets
from functools import wraps

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from werkzeug.utils import secure_filename
from markupsafe import Markup, escape
from werkzeug.security import check_password_hash, generate_password_hash

import db
from schema import (CONTENT_TYPES, SECTION_FIELDS, SECTION_KEYS,
                    SETTINGS_GROUPS, settings_fields)

# Menú principal. Un elemento con "children" despliega un submenú;
# "endpoint" en None hace que el rótulo no sea un enlace (solo abre el submenú).
NAV = [
    {"endpoint": "campana", "label": "DOMUND", "children": None},
    {"endpoint": "quienes_somos", "label": "Quiénes somos", "children": "areas"},
    {"endpoint": "programas", "label": "Programas", "children": None},
    {"endpoint": None, "label": "Noticias y eventos",
     "children": [("noticias", "Noticias"), ("eventos", "Eventos")]},
    {"endpoint": "territorio", "label": "Presencia territorial", "children": None},
    {"endpoint": "documentacion", "label": "Documentación", "children": None},
]

app = Flask(__name__)
app.teardown_appcontext(db.close_db)

# La cookie de sesión no viaja en peticiones de otros sitios ni la lee el JS.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("CMS_COOKIE_SECURE", "") == "1",
)


# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

def bootstrap():
    """Espera a la base, crea el esquema, siembra y asegura un usuario."""
    if db.USING_POSTGRES:
        db.esperar_base_de_datos()

    with app.app_context():
        db.init_db()

        secret = os.environ.get("CMS_SECRET_KEY") or db.get_setting("secret_key")
        if not secret:
            secret = secrets.token_hex(32)
            db.set_setting("secret_key", secret)
        app.secret_key = secret

        usuario = os.environ.get("CMS_ADMIN_USER", "admin")
        clave = os.environ.get("CMS_ADMIN_PASSWORD", "admin1234")
        if db.ensure_initial_user(usuario, "Administrador", generate_password_hash(clave)):
            print("Usuario inicial creado: %s" % usuario)


# ---------------------------------------------------------------------------
# Utilidades de plantilla
# ---------------------------------------------------------------------------

@app.template_filter("nl2br")
def nl2br(value):
    """Convierte saltos de línea en <br>, escapando el resto."""
    if value is None:
        return ""
    parts = escape(value).split("\n")
    return Markup("<br>".join(parts))


def _bloques(texto):
    """Parte un texto en párrafos, aceptando saltos simples o dobles y \r\n."""
    if not texto:
        return []
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    return [b.strip() for b in texto.split("\n") if b.strip()]


def _es_subtitulo(linea):
    return len(linea) <= 30 and not linea.endswith((".", ":", "?", "!", "»", "”", '"'))


@app.template_filter("parrafos")
def parrafos(texto):
    """Texto plano a HTML: líneas cortas sin punto final pasan a subtítulo."""
    html = []
    for bloque in _bloques(texto):
        if _es_subtitulo(bloque):
            html.append(Markup("<h2>%s</h2>") % bloque.capitalize())
        elif bloque.startswith(("“", '"', "«")):
            html.append(Markup('<blockquote>%s</blockquote>') % bloque)
        else:
            html.append(Markup("<p>%s</p>") % bloque)
    return Markup("\n").join(html)


@app.template_filter("primer_parrafo")
def primer_parrafo(texto):
    bloques = _bloques(texto)
    return bloques[0] if bloques else ""


@app.template_filter("resto_parrafos")
def resto_parrafos(texto):
    return "\n".join(_bloques(texto)[1:])


@app.context_processor
def inject_nav():
    """El menú lateral del panel se construye desde el esquema."""
    if not (request.endpoint or "").startswith("admin"):
        return {}
    return {"content_types": CONTENT_TYPES, "current_user": usuario_actual()}


@app.context_processor
def inject_site():
    """Cabecera, menú y pie: lo que necesita base.html en toda página pública."""
    if (request.endpoint or "").startswith("admin"):
        return {}
    menu = []
    for item in NAV:
        hijos = []
        if item["children"] == "areas":
            hijos = [("quienes_somos", "Las cuatro áreas", None)] + [
                ("area_detalle", fila["title"], fila["id"])
                for fila in db.list_rows("areas", only_published=True)
            ]
        elif item["children"]:
            hijos = [(ep, etiqueta, None) for ep, etiqueta in item["children"]]
        menu.append({"endpoint": item["endpoint"], "label": item["label"], "children": hijos})

    return {
        "nav": menu,
        "settings": db.all_settings(),
        "sections": db.all_sections(),
        "footer_links": {
            clave: db.rows_by("footer_links", "column_key", clave)
            for clave in ("institucion", "programas", "contacto")
        },
        "legal_links": db.list_rows("legal_links", only_published=True),
    }


UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".pdf"}
MAX_SUBIDA = 8 * 1024 * 1024          # 8 MB por archivo
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def guardar_archivo(archivo):
    """Guarda una subida y devuelve su ruta pública, o None si no sirve."""
    if not archivo or not archivo.filename:
        return None

    nombre = secure_filename(archivo.filename)
    base, extension = os.path.splitext(nombre)
    extension = extension.lower()
    if extension not in EXTENSIONES:
        raise ValueError("Formato no admitido: usa JPG, PNG, WEBP, GIF, SVG o PDF.")

    base = re.sub(r"[^a-z0-9-]+", "-", base.lower()).strip("-") or "archivo"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    destino = "%s%s" % (base, extension)
    contador = 2
    while os.path.exists(os.path.join(UPLOAD_DIR, destino)):
        destino = "%s-%d%s" % (base, contador, extension)
        contador += 1

    archivo.save(os.path.join(UPLOAD_DIR, destino))
    return url_for("static", filename="uploads/%s" % destino)


def collect_con_archivos(fields, form, files, fila_actual=None):
    """Como collect, pero los campos de imagen conservan o reemplazan el archivo."""
    valores = collect(fields, form)
    for campo in fields:
        if campo["type"] != "image":
            continue
        nombre = campo["name"]
        subido = guardar_archivo(files.get(nombre))
        if subido:
            valores[nombre] = subido
        elif form.get(nombre + "__borrar"):
            valores[nombre] = ""
        else:
            valores[nombre] = (fila_actual or {}).get(nombre, "") or form.get(nombre, "")
    return valores


def collect(fields, form):
    """Extrae los valores de un formulario según una lista de campos."""
    return {field["name"]: form.get(field["name"], "").strip() for field in fields}


def collect_present(fields, form, prefix=""):
    """Como collect, pero ignora los campos que el formulario no ha enviado.

    Evita que un envío parcial vacíe ajustes que no estaban en pantalla.
    """
    values = {}
    for field in fields:
        key = prefix + field["name"]
        if key in form:
            values[field["name"]] = form.get(key, "").strip()
    return values


def usuario_actual():
    """Usuario de la sesión, o None si no hay sesión válida."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    usuario = db.get_user(user_id)
    if usuario is None or not usuario["active"]:
        return None
    return usuario


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if usuario_actual() is None:
            session.clear()
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def content_type_or_404(table):
    spec = CONTENT_TYPES.get(table)
    if spec is None:
        abort(404)
    return spec


# ---------------------------------------------------------------------------
# Páginas públicas
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    documentos = db.list_rows("documents", only_published=True)
    return render_template(
        "index.html",
        slides=db.list_rows("slides", only_published=True),
        areas=db.list_rows("areas", only_published=True),
        voices=db.list_rows("voices", only_published=True),
        counters=db.list_rows("counters", only_published=True),
        projects=db.list_rows("projects", only_published=True),
        news=db.list_rows("news", only_published=True),
        events=db.list_rows("events", only_published=True),
        bulletins=[fila for fila in documentos if fila["doc_group"] == "boletin"],
        reports=[fila for fila in documentos if fila["doc_group"] == "memoria"],
    )


# Los pasos del recorrido del dinero y la cadena de gobierno salen del folleto.
PASOS_ESTRUCTURA = [
    {"title": "Secretariado Internacional, en Roma",
     "body": "Las cuatro Obras tienen su gobierno central en el Secretariado Internacional "
             "de las OMP, en Via di Propaganda 1. Depende del Dicasterio para la "
             "Evangelización y desde ahí se administra el Fondo Universal de Solidaridad."},
    {"title": "La colecta viaja íntegra",
     "body": "Todo lo que se recoge el día del DOMUND en más de 140 países va completo al "
             "Fondo Universal de Solidaridad. Es la colecta más universal de la Iglesia."},
    {"title": "Asamblea General, cada mayo",
     "body": "Los Directores Nacionales de todo el mundo se reúnen en Roma y presentan los "
             "proyectos de las cuatro Obras."},
    {"title": "Se reparte según necesidad",
     "body": "Los fondos se asignan según la necesidad de cada territorio, no según quién "
             "aportó más. Así llegan a las 1.100 diócesis más pobres del planeta."},
]

CIFRAS_CAMPANA = [
    {"number": "100", "label": "Años de DOMUND desde 1926"},
    {"number": "140+", "label": "Países donde se celebra la jornada"},
    {"number": "1.100", "label": "Diócesis sostenidas con la colecta"},
]


@app.route("/domund")
def campana():
    return render_template(
        "campana.html",
        founders=db.list_rows("founders", only_published=True),
        structure_steps=PASOS_ESTRUCTURA,
        campaign_facts=CIFRAS_CAMPANA,
    )


@app.route("/quienes-somos")
def quienes_somos():
    return render_template(
        "quienes_somos.html",
        areas=db.list_rows("areas", only_published=True),
        counters=db.list_rows("counters", only_published=True),
    )


@app.route("/programas")
def programas():
    return render_template(
        "programas.html",
        projects=db.list_rows("projects", only_published=True),
    )


def _url_o_detalle(fila, endpoint):
    """El enlace guardado manda; si es un marcador vacío, va a la página de detalle."""
    if fila.get("href") and fila["href"] != "#":
        return fila["href"]
    return url_for(endpoint, item_id=fila["id"])


@app.route("/noticias")
def noticias():
    filas = db.list_rows("news", only_published=True)
    return render_template(
        "listado.html", titulo=db.get_setting("news_col_title", "Noticias"),
        filas=[dict(f, url=_url_o_detalle(f, "noticia_detalle")) for f in filas],
        vacio="Sin noticias por ahora.",
    )


@app.route("/eventos")
def eventos():
    filas = db.list_rows("events", only_published=True)
    return render_template(
        "listado.html", titulo=db.get_setting("events_col_title", "Eventos"),
        filas=[dict(f, url=_url_o_detalle(f, "evento_detalle")) for f in filas],
        vacio="Sin eventos convocados.",
    )


def _detalle(table, item_id, **extra):
    fila = db.get_row(table, item_id)
    if fila is None or not fila["published"]:
        abort(404)
    return render_template("detalle.html", fila=fila, **extra)


@app.route("/noticias/<int:item_id>")
def noticia_detalle(item_id):
    return _detalle("news", item_id, kicker="Noticias",
                    volver=("noticias", "Todas las noticias"))


@app.route("/eventos/<int:item_id>")
def evento_detalle(item_id):
    return _detalle("events", item_id, kicker="Eventos",
                    volver=("eventos", "Todos los eventos"))


@app.route("/territorio/<int:item_id>")
def voz_detalle(item_id):
    return _detalle("voices", item_id, kicker=None,
                    volver=("territorio", "Todas las voces"))


@app.route("/programas/<int:item_id>")
def proyecto_detalle(item_id):
    return _detalle("projects", item_id, kicker=None,
                    volver=("programas", "Todos los proyectos"))


@app.route("/quienes-somos/<int:item_id>")
def area_detalle(item_id):
    return _detalle("areas", item_id, kicker="Áreas de trabajo",
                    volver=("quienes_somos", "Todas las áreas"))


@app.route("/territorio")
def territorio():
    return render_template(
        "territorio.html",
        voices=db.list_rows("voices", only_published=True),
    )


@app.route("/documentacion")
def documentacion():
    documentos = db.list_rows("documents", only_published=True)
    return render_template(
        "documentacion.html",
        bulletins=[fila for fila in documentos if fila["doc_group"] == "boletin"],
        reports=[fila for fila in documentos if fila["doc_group"] == "memoria"],
    )


# ---------------------------------------------------------------------------
# Sesión del panel
# ---------------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        nombre = request.form.get("username", "").strip()
        clave = request.form.get("password", "")
        usuario = db.get_user_by_username(nombre) if nombre else None

        if usuario and usuario["active"] and check_password_hash(usuario["password_hash"], clave):
            session.clear()
            session["user_id"] = usuario["id"]
            destino = request.args.get("next") or url_for("admin_home")
            if not destino.startswith("/admin"):
                destino = url_for("admin_home")
            return redirect(destino)

        if usuario and not usuario["active"]:
            flash("Esa cuenta está desactivada.", "error")
        else:
            flash("Usuario o contraseña incorrectos.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ---------------------------------------------------------------------------
# Panel: inicio
# ---------------------------------------------------------------------------

@app.route("/admin/")
@login_required
def admin_home():
    resumen = [
        {"table": table, "label": spec["label"], "total": db.count_rows(table)}
        for table, spec in CONTENT_TYPES.items()
    ]
    return render_template("admin/index.html", resumen=resumen)


@app.route("/admin/guia")
@login_required
def admin_guide():
    """Manual de uso, dentro del propio panel."""
    return render_template("admin/guide.html")


# ---------------------------------------------------------------------------
# Panel: contenido genérico
# ---------------------------------------------------------------------------

@app.route("/admin/c/<table>")
@login_required
def admin_list(table):
    spec = content_type_or_404(table)
    return render_template(
        "admin/list.html", table=table, spec=spec, rows=db.list_rows(table)
    )


@app.route("/admin/c/<table>/nuevo", methods=["GET", "POST"])
@login_required
def admin_create(table):
    spec = content_type_or_404(table)
    if request.method == "POST":
        try:
            valores = collect_con_archivos(spec["fields"], request.form, request.files)
        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("admin_create", table=table))
        db.create(table, valores, published=1 if request.form.get("published") else 0)
        flash("Se ha creado el registro.", "ok")
        return redirect(url_for("admin_list", table=table))

    blank = {field["name"]: field.get("default", "") for field in spec["fields"]}
    blank["published"] = 1
    return render_template("admin/form.html", table=table, spec=spec, row=blank, is_new=True)


@app.route("/admin/c/<table>/<int:row_id>", methods=["GET", "POST"])
@login_required
def admin_edit(table, row_id):
    spec = content_type_or_404(table)
    row = db.get_row(table, row_id)
    if row is None:
        abort(404)

    if request.method == "POST":
        try:
            valores = collect_con_archivos(spec["fields"], request.form, request.files, row)
        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("admin_edit", table=table, row_id=row_id))
        db.update(table, row_id, valores,
                  published=1 if request.form.get("published") else 0)
        flash("Cambios guardados.", "ok")
        return redirect(url_for("admin_list", table=table))

    return render_template("admin/form.html", table=table, spec=spec,
                           row=dict(row), is_new=False)


@app.route("/admin/c/<table>/<int:row_id>/eliminar", methods=["POST"])
@login_required
def admin_delete(table, row_id):
    content_type_or_404(table)
    db.delete(table, row_id)
    flash("Registro eliminado.", "ok")
    return redirect(url_for("admin_list", table=table))


@app.route("/admin/c/<table>/<int:row_id>/visibilidad", methods=["POST"])
@login_required
def admin_toggle(table, row_id):
    content_type_or_404(table)
    db.toggle_published(table, row_id)
    return redirect(url_for("admin_list", table=table))


@app.route("/admin/c/<table>/<int:row_id>/mover/<direction>", methods=["POST"])
@login_required
def admin_move(table, row_id, direction):
    content_type_or_404(table)
    if direction not in ("up", "down"):
        abort(400)
    db.move(table, row_id, direction)
    return redirect(url_for("admin_list", table=table))


# ---------------------------------------------------------------------------
# Panel: encabezados de sección
# ---------------------------------------------------------------------------

@app.route("/admin/secciones", methods=["GET", "POST"])
@login_required
def admin_sections():
    if request.method == "POST":
        payload = {}
        for key, _label in SECTION_KEYS:
            values = collect_present(SECTION_FIELDS, request.form, prefix=key + "__")
            if values:
                payload[key] = values
        db.save_sections(payload)
        flash("Encabezados actualizados.", "ok")
        return redirect(url_for("admin_sections"))

    return render_template("admin/sections.html", sections=db.all_sections(),
                           section_keys=SECTION_KEYS, section_fields=SECTION_FIELDS)


# ---------------------------------------------------------------------------
# Panel: ajustes generales
# ---------------------------------------------------------------------------

@app.route("/admin/ajustes", methods=["GET", "POST"])
@login_required
def admin_settings():
    if request.method == "POST":
        db.save_settings(collect_present(settings_fields(), request.form))
        flash("Ajustes guardados.", "ok")
        return redirect(url_for("admin_settings"))

    return render_template("admin/settings.html", groups=SETTINGS_GROUPS,
                           values=db.all_settings())


@app.route("/admin/contrasena", methods=["GET", "POST"])
@login_required
def admin_password():
    """Cada quien cambia su propia contraseña."""
    usuario = usuario_actual()
    if request.method == "POST":
        actual = request.form.get("current", "")
        nueva = request.form.get("new", "")
        repetida = request.form.get("repeat", "")

        if not check_password_hash(usuario["password_hash"], actual):
            flash("La contraseña actual no es correcta.", "error")
        elif len(nueva) < 8:
            flash("La nueva contraseña debe tener al menos 8 caracteres.", "error")
        elif nueva != repetida:
            flash("Las dos contraseñas nuevas no coinciden.", "error")
        else:
            db.set_user_password(usuario["id"], generate_password_hash(nueva))
            flash("Contraseña actualizada.", "ok")
            return redirect(url_for("admin_home"))

    return render_template("admin/password.html")


# ---------------------------------------------------------------------------
# Panel: usuarios
# ---------------------------------------------------------------------------

ROLES = [("admin", "Administrador"), ("editor", "Editor")]


@app.route("/admin/usuarios")
@login_required
def admin_users():
    return render_template("admin/users.html", users=db.list_users(), roles=dict(ROLES))


@app.route("/admin/usuarios/nuevo", methods=["GET", "POST"])
@login_required
def admin_user_create():
    if request.method == "POST":
        datos = {
            "username": request.form.get("username", "").strip().lower(),
            "name": request.form.get("name", "").strip(),
            "role": request.form.get("role", "admin"),
            "active": 1 if request.form.get("active") else 0,
        }
        clave = request.form.get("password", "")

        error = None
        if not datos["username"]:
            error = "El usuario es obligatorio."
        elif db.get_user_by_username(datos["username"]):
            error = "Ya existe un usuario con ese nombre."
        elif len(clave) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."

        if error:
            flash(error, "error")
            return render_template("admin/user_form.html", user=datos, roles=ROLES, is_new=True)

        db.create_user(datos["username"], datos["name"], generate_password_hash(clave),
                       datos["role"], datos["active"])
        flash("Usuario creado.", "ok")
        return redirect(url_for("admin_users"))

    return render_template("admin/user_form.html",
                           user={"username": "", "name": "", "role": "admin", "active": 1},
                           roles=ROLES, is_new=True)


@app.route("/admin/usuarios/<int:user_id>", methods=["GET", "POST"])
@login_required
def admin_user_edit(user_id):
    usuario = db.get_user(user_id)
    if usuario is None:
        abort(404)

    if request.method == "POST":
        nombre_usuario = request.form.get("username", "").strip().lower()
        nombre = request.form.get("name", "").strip()
        rol = request.form.get("role", "admin")
        activo = 1 if request.form.get("active") else 0
        clave = request.form.get("password", "")

        existente = db.get_user_by_username(nombre_usuario)
        error = None
        if not nombre_usuario:
            error = "El usuario es obligatorio."
        elif existente and existente["id"] != user_id:
            error = "Ya existe un usuario con ese nombre."
        elif clave and len(clave) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        elif not activo and usuario["id"] == session.get("user_id"):
            error = "No puedes desactivar tu propia cuenta."
        elif not activo and usuario["active"] and db.count_users(only_active=True) <= 1:
            error = "No puedes desactivar al único usuario activo."

        if error:
            flash(error, "error")
        else:
            db.update_user(user_id, nombre_usuario, nombre, rol, activo)
            if clave:
                db.set_user_password(user_id, generate_password_hash(clave))
            flash("Cambios guardados.", "ok")
            return redirect(url_for("admin_users"))

    return render_template("admin/user_form.html", user=db.get_user(user_id),
                           roles=ROLES, is_new=False)


@app.route("/admin/usuarios/<int:user_id>/eliminar", methods=["POST"])
@login_required
def admin_user_delete(user_id):
    if user_id == session.get("user_id"):
        flash("No puedes eliminar tu propia cuenta.", "error")
    elif db.count_users() <= 1:
        flash("Tiene que quedar al menos un usuario.", "error")
    else:
        db.delete_user(user_id)
        flash("Usuario eliminado.", "ok")
    return redirect(url_for("admin_users"))


bootstrap()


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))

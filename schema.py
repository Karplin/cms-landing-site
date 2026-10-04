# -*- coding: utf-8 -*-
"""Definición del contenido gestionable por el CMS.

Todo el panel de administración (listados, formularios y esquema de la base de
datos) se genera a partir de las estructuras de este módulo. Añadir un campo
nuevo aquí basta para que aparezca en el formulario, en la tabla SQLite y en la
plantilla pública.
"""

# ---------------------------------------------------------------------------
# Tipos de contenido con varios registros (listado + alta + edición + orden)
# ---------------------------------------------------------------------------

CONTENT_TYPES = {
    "slides": {
        "label": "Diapositivas del hero",
        "singular": "diapositiva",
        "help": "Cada diapositiva ocupa la portada durante siete segundos.",
        "list_columns": ["title_light", "title_strong", "meta"],
        "fields": [
            {"name": "title_light", "label": "Titular · línea ligera", "type": "text", "required": True},
            {"name": "title_strong", "label": "Titular · línea destacada", "type": "textarea", "rows": 2,
             "help": "Se muestra en negrita. Cada salto de línea es un renglón nuevo."},
            {"name": "meta", "label": "Fecha o lugar", "type": "text"},
            {"name": "cta_label", "label": "Texto del botón", "type": "text"},
            {"name": "cta_href", "label": "Enlace del botón", "type": "text", "default": "#"},
            {"name": "cta_icon", "label": "Icono del botón", "type": "select",
             "options": [("play", "Reproducir"), ("download", "Descargar"), ("none", "Sin icono")],
             "default": "play"},
            {"name": "quote_strong", "label": "Cita · tramo destacado", "type": "text"},
            {"name": "quote_rest", "label": "Cita · resto", "type": "textarea", "rows": 2},
            {"name": "author", "label": "Atribución de la cita", "type": "text"},
        ],
    },
    "areas": {
        "label": "Áreas de trabajo",
        "singular": "área",
        "help": "Las tarjetas de la primera franja crema.",
        "list_columns": ["title", "icon"],
        "fields": [
            {"name": "icon", "label": "Icono", "type": "select",
             "options": [("educacion", "Educación"), ("salud", "Salud"), ("agua", "Agua"),
                         ("liderazgo", "Liderazgo")],
             "default": "educacion"},
            {"name": "title", "label": "Título", "type": "text", "required": True},
            {"name": "summary", "label": "Resumen para la tarjeta", "type": "textarea", "rows": 2,
             "help": "Una o dos frases. Es lo que se ve en la tarjeta; el texto completo va en su página."},
            {"name": "body", "label": "Texto completo", "type": "textarea", "rows": 14,
             "help": "Se muestra en la página propia del área. Una línea corta sin punto final "
                     "(por ejemplo «Historia» o «Misión») se convierte en subtítulo."},
            {"name": "photo", "label": "Imagen", "type": "image",
             "help": "Opcional. Sustituye al icono en la tarjeta."},
            {"name": "link_label", "label": "Texto del enlace", "type": "text", "default": "Conocer el área"},
            {"name": "link_href", "label": "Enlace", "type": "text", "default": "#proyectos"},
        ],
    },
    "voices": {
        "label": "Voces del territorio",
        "singular": "voz",
        "help": "Carrusel horizontal de noticias de las sedes.",
        "list_columns": ["place", "date_label", "title"],
        "fields": [
            {"name": "place", "label": "Sede o país", "type": "text", "required": True},
            {"name": "date_label", "label": "Fecha", "type": "text", "help": "Por ejemplo: 18 Ago 2026"},
            {"name": "title", "label": "Titular", "type": "text", "required": True},
            {"name": "body", "label": "Entradilla", "type": "textarea", "rows": 3},
        ],
    },
    "counters": {
        "label": "Contadores",
        "singular": "contador",
        "help": "Las cifras grandes de la franja crema.",
        "list_columns": ["number", "label"],
        "fields": [
            {"name": "number", "label": "Cifra", "type": "text", "required": True,
             "help": "Se muestra tal cual: usa el separador de miles que prefieras."},
            {"name": "label", "label": "Descripción", "type": "text", "required": True},
        ],
    },
    "projects": {
        "label": "Proyectos",
        "singular": "proyecto",
        "help": "Tarjetas de la sección Nuestros proyectos.",
        "list_columns": ["area_label", "title", "place"],
        "fields": [
            {"name": "area_label", "label": "Área", "type": "text", "required": True},
            {"name": "title", "label": "Título", "type": "text", "required": True},
            {"name": "place", "label": "Lugar", "type": "text"},
            {"name": "href", "label": "Enlace", "type": "text", "default": "#"},
            {"name": "tone", "label": "Color de cabecera", "type": "select",
             "options": [("teal", "Verde azulado"), ("amber", "Terracota"), ("green", "Verde"),
                         ("plum", "Ciruela")],
             "default": "teal"},
        ],
    },
    "news": {
        "label": "Noticias",
        "singular": "noticia",
        "list_columns": ["day", "month", "title"],
        "fields": [
            {"name": "day", "label": "Día", "type": "text", "required": True},
            {"name": "month", "label": "Mes", "type": "text", "required": True,
             "help": "Abreviado: Ago, Sep, Oct..."},
            {"name": "title", "label": "Titular", "type": "text", "required": True},
            {"name": "summary", "label": "Entradilla", "type": "textarea", "rows": 3},
            {"name": "href", "label": "Enlace", "type": "text", "default": "#"},
        ],
    },
    "events": {
        "label": "Eventos",
        "singular": "evento",
        "list_columns": ["day", "month", "title"],
        "fields": [
            {"name": "day", "label": "Día", "type": "text", "required": True},
            {"name": "month", "label": "Mes", "type": "text", "required": True},
            {"name": "title", "label": "Título", "type": "text", "required": True},
            {"name": "summary", "label": "Descripción", "type": "textarea", "rows": 3},
            {"name": "href", "label": "Enlace", "type": "text", "default": "#"},
        ],
    },
    "documents": {
        "label": "Documentación",
        "singular": "documento",
        "help": "Boletines y memorias descargables.",
        "list_columns": ["doc_group", "title", "size_label"],
        "fields": [
            {"name": "doc_group", "label": "Columna", "type": "select",
             "options": [("boletin", "Boletines"), ("memoria", "Memorias anuales")],
             "default": "boletin"},
            {"name": "title", "label": "Título", "type": "text", "required": True},
            {"name": "meta", "label": "Descripción breve", "type": "text"},
            {"name": "size_label", "label": "Texto del enlace", "type": "text",
             "default": "Descargar", "help": "Por ejemplo: Descargar (4,9 MB)"},
            {"name": "href", "label": "Enlace al archivo", "type": "text", "default": "#"},
        ],
    },
    "founders": {
        "label": "Fundadores",
        "singular": "fundador",
        "help": "Los rostros detrás de cada Obra. Salen en la página de la campaña.",
        "list_columns": ["name", "work", "years"],
        "fields": [
            {"name": "photo", "label": "Retrato", "type": "image"},
            {"name": "name", "label": "Nombre", "type": "text", "required": True},
            {"name": "years", "label": "Años", "type": "text", "help": "Por ejemplo: 1799-1862"},
            {"name": "work", "label": "Obra que fundó", "type": "text", "required": True},
            {"name": "work_year", "label": "Año de fundación", "type": "text"},
            {"name": "note", "label": "Nota breve", "type": "textarea", "rows": 2},
        ],
    },
    "footer_links": {
        "label": "Enlaces del pie",
        "singular": "enlace",
        "help": "Las tres columnas de enlaces del pre-footer.",
        "list_columns": ["column_key", "label", "href"],
        "fields": [
            {"name": "column_key", "label": "Columna", "type": "select",
             "options": [("institucion", "Institución"), ("programas", "Programas"),
                         ("contacto", "Contacto")],
             "default": "institucion"},
            {"name": "label", "label": "Texto", "type": "text", "required": True},
            {"name": "href", "label": "Enlace", "type": "text", "default": "#"},
        ],
    },
    "legal_links": {
        "label": "Enlaces legales",
        "singular": "enlace legal",
        "help": "La línea inferior del pie.",
        "list_columns": ["label", "href"],
        "fields": [
            {"name": "label", "label": "Texto", "type": "text", "required": True},
            {"name": "href", "label": "Enlace", "type": "text", "default": "#"},
        ],
    },
}

# Columnas que el CMS anade a todas las tablas de contenido.
BASE_COLUMNS = ["id", "position", "published"]

# ---------------------------------------------------------------------------
# Encabezados de sección (registros fijos: solo se editan)
# ---------------------------------------------------------------------------

SECTION_KEYS = [
    ("areas", "Áreas de trabajo"),
    ("voices", "Voces del territorio"),
    ("counters", "Contadores"),
    ("projects", "Proyectos"),
    ("news", "Noticias y eventos"),
    ("documents", "Documentación"),
    ("campaign", "Campaña (DOMUND)"),
    ("founders", "Fundadores"),
    ("structure", "Estructura de las Obras"),
]

SECTION_FIELDS = [
    {"name": "eyebrow", "label": "Antetítulo", "type": "text"},
    {"name": "title", "label": "Título", "type": "text", "required": True},
    {"name": "subtitle", "label": "Bajada", "type": "textarea", "rows": 2},
]

# ---------------------------------------------------------------------------
# Ajustes generales (tabla clave/valor)
# ---------------------------------------------------------------------------

SETTINGS_GROUPS = [
    {
        "label": "Identidad",
        "fields": [
            {"name": "site_title", "label": "Título de la pestaña", "type": "text"},
            {"name": "brand_name", "label": "Nombre de la organización", "type": "textarea", "rows": 2,
             "help": "Cada salto de línea es un renglón del logotipo."},
            {"name": "brand_sub", "label": "Bajada del logotipo", "type": "text"},
        ],
    },
    {
        "label": "Cabecera",
        "fields": [
            {"name": "header_login", "label": "Texto del botón de acceso", "type": "text"},
        ],
    },
    {
        "label": "Proyectos",
        "fields": [
            {"name": "projects_cta_label", "label": "Botón bajo los proyectos", "type": "text"},
            {"name": "projects_cta_href", "label": "Enlace del botón", "type": "text"},
        ],
    },
    {
        "label": "Noticias, eventos y documentacion",
        "fields": [
            {"name": "news_col_title", "label": "Título columna noticias", "type": "text"},
            {"name": "news_col_link", "label": "Enlace columna noticias", "type": "text"},
            {"name": "events_col_title", "label": "Título columna eventos", "type": "text"},
            {"name": "events_col_link", "label": "Enlace columna eventos", "type": "text"},
            {"name": "docs_col1_title", "label": "Título columna boletines", "type": "text"},
            {"name": "docs_col1_link", "label": "Enlace columna boletines", "type": "text"},
            {"name": "docs_col2_title", "label": "Título columna memorias", "type": "text"},
            {"name": "docs_col2_link", "label": "Enlace columna memorias", "type": "text"},
        ],
    },
    {
        "label": "Campaña (DOMUND)",
        "fields": [
            {"name": "campaign_poster", "label": "Afiche", "type": "image"},
            {"name": "campaign_motto", "label": "Lema", "type": "text"},
            {"name": "campaign_date", "label": "Fecha de la jornada", "type": "text"},
            {"name": "campaign_call", "label": "Llamada final", "type": "text"},
            {"name": "campaign_cta_label", "label": "Texto del botón", "type": "text"},
            {"name": "campaign_cta_href", "label": "Enlace del botón", "type": "text",
             "help": "Por ejemplo, el folleto en PDF."},
        ],
    },
    {
        "label": "Pie de página",
        "fields": [
            {"name": "footer_col_institucion", "label": "Título columna 1", "type": "text"},
            {"name": "footer_col_programas", "label": "Título columna 2", "type": "text"},
            {"name": "footer_col_contacto", "label": "Título columna 3", "type": "text"},
            {"name": "address", "label": "Dirección", "type": "textarea", "rows": 3},
            {"name": "contact_line", "label": "Teléfono y correo", "type": "text"},
            {"name": "social_youtube", "label": "Enlace de YouTube", "type": "text"},
            {"name": "social_linkedin", "label": "Enlace de LinkedIn", "type": "text"},
            {"name": "social_mail", "label": "Enlace del boletin", "type": "text"},
            {"name": "copyright", "label": "Linea de copyright", "type": "text"},
        ],
    },
    {
        "label": "Aviso de cookies",
        "fields": [
            {"name": "cookie_title", "label": "Título", "type": "text"},
            {"name": "cookie_text", "label": "Texto", "type": "textarea", "rows": 3},
            {"name": "cookie_button", "label": "Botón", "type": "text"},
        ],
    },
]


def settings_fields():
    """Todos los campos de ajustes, aplanados."""
    return [field for group in SETTINGS_GROUPS for field in group["fields"]]


def field_default(field):
    return field.get("default", "")

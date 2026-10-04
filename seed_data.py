# -*- coding: utf-8 -*-
"""Contenido inicial. Solo se inserta la primera vez que se crea cms.db."""

SEED = {
    "settings": {
        "site_title": "Instituto de Cooperación Regional",
        "brand_name": "Instituto de\nCooperación Regional",
        "brand_sub": "Sedes territoriales",
        "header_login": "Acceso",
        "projects_cta_label": "Ver todos los proyectos",
        "projects_cta_href": "/programas",
        "news_col_title": "Noticias",
        "news_col_link": "Todas",
        "events_col_title": "Eventos",
        "events_col_link": "Todos",
        "docs_col1_title": "Boletines",
        "docs_col1_link": "Leer todos",
        "docs_col2_title": "Memorias anuales",
        "docs_col2_link": "Ver el archivo",
        "campaign_poster": "/static/uploads/afiche-domund-2026.jpg",
        "campaign_motto": "Sinodalidad, unidos en el Espíritu para anunciar el Evangelio",
        "campaign_date": "Domingo 18 de octubre de 2026",
        "campaign_call": "Oración, sacrificio y ofrenda.",
        "campaign_cta_label": "Descargar el folleto",
        "campaign_cta_href": "/static/uploads/brochure-domund.pdf",
        "footer_col_institucion": "Institución",
        "footer_col_programas": "Programas",
        "footer_col_contacto": "Contacto",
        "address": "Sede central · Calle 34 n.º 12-48\nBogotá, Colombia",
        "contact_line": "+57 601 000 0000 · contacto@icr.example",
        "social_youtube": "#",
        "social_linkedin": "#",
        "social_mail": "#",
        "copyright": "© 2026 Instituto de Cooperación Regional — Todos los derechos reservados",
        "cookie_title": "Política de cookies",
        "cookie_text": "Este portal usa cookies técnicas necesarias para la navegación. "
                       "No se activa ninguna cookie de análisis ni de terceros sin tu consentimiento.",
        "cookie_button": "De acuerdo",
    },

    "sections": {
        "areas": {
            "eyebrow": "Quiénes somos",
            "title": "Las cuatro áreas de trabajo",
            "subtitle": "Un mismo método en veintiocho territorios: acompañar a las organizaciones "
                        "que ya existen, en lugar de sustituirlas.",
        },
        "voices": {
            "eyebrow": "Noticias e iniciativas de las sedes",
            "title": "Voces del territorio",
            "subtitle": "",
        },
        "counters": {
            "eyebrow": "Con el apoyo de todos",
            "title": "En el último año hemos podido acompañar…",
            "subtitle": "",
        },
        "projects": {
            "eyebrow": "Programas",
            "title": "Nuestros proyectos",
            "subtitle": "Cada proyecto se formula con la organización local que lo va a sostener "
                        "y se publica con su presupuesto abierto.",
        },
        "news": {
            "eyebrow": "Actualidad",
            "title": "Noticias y eventos",
            "subtitle": "",
        },
        "documents": {
            "eyebrow": "Documentación",
            "title": "Boletines y memorias",
            "subtitle": "",
        },
        "campaign": {
            "eyebrow": "Domingo Mundial de las Misiones",
            "title": "DOMUND: cien años de una jornada que une al mundo",
            "subtitle": "En 1926 el Papa Pío XI, el Papa de las Misiones, instituyó la Jornada "
                        "Misionera Mundial a petición de la Obra de la Propagación de la Fe. "
                        "La idea era simple: que un domingo de octubre toda la Iglesia del mundo "
                        "rece y dé limosna por las misiones.",
        },
        "founders": {
            "eyebrow": "Fundadores de la OMP",
            "title": "Cuatro personas, cuatro Obras",
            "subtitle": "Cada una de las Obras Misionales Pontificias nació del impulso de "
                        "alguien concreto.",
        },
        "structure": {
            "eyebrow": "Cómo funciona",
            "title": "Estructura de las Obras",
            "subtitle": "Todo lo que se recoge en octubre llega a Roma y desde Roma se reparte "
                        "a las 1.100 diócesis más pobres del planeta.",
        },
    },

    "slides": [
        {
            "title_light": "Encuentro",
            "title_strong": "Regional de\nCooperación",
            "meta": "Cartagena · 14 al 17 de octubre de 2026",
            "cta_label": "Ver el programa",
            "cta_href": "/noticias",
            "cta_icon": "play",
            "quote_strong": "«Ninguna comunidad avanza sola:",
            "quote_rest": "avanza cuando comparte lo que ya sabe hacer»",
            "author": "Declaración de apertura, 2026",
        },
        {
            "title_light": "Memoria",
            "title_strong": "Anual\n2025",
            "meta": "Cuatro áreas · veintiocho territorios",
            "cta_label": "Descargar la memoria",
            "cta_href": "/documentacion",
            "cta_icon": "download",
            "quote_strong": "«1 284 proyectos acompañados",
            "quote_rest": "y 312 organizaciones locales fortalecidas en un solo año»",
            "author": "Balance de gestión 2025",
        },
        {
            "title_light": "Escuela de",
            "title_strong": "Liderazgo\nJuvenil",
            "meta": "Convocatoria abierta hasta el 30 de septiembre",
            "cta_label": "Conocer la convocatoria",
            "cta_href": "/programas",
            "cta_icon": "play",
            "quote_strong": "«Formamos a quienes ya están",
            "quote_rest": "sosteniendo el trabajo en sus propios barrios»",
            "author": "Área de Formación y Liderazgo",
        },
    ],

    "areas": [
        {
            "icon": "educacion",
            "title": "Educación Comunitaria",
            "body": "Acompañamos escuelas rurales, aulas multigrado y bibliotecas comunitarias "
                    "en zonas de difícil acceso.",
            "link_label": "Conocer el área",
            "link_href": "/programas",
        },
        {
            "icon": "salud",
            "title": "Salud Territorial",
            "body": "Brigadas periódicas, formación de promotores de salud y acceso a servicios "
                    "básicos donde no llega la red pública.",
            "link_label": "Conocer el área",
            "link_href": "/programas",
        },
        {
            "icon": "agua",
            "title": "Agua y Territorio",
            "body": "Sistemas de agua potable, saneamiento básico y cuidado colectivo de cuencas "
                    "junto a las juntas veredales.",
            "link_label": "Conocer el área",
            "link_href": "/programas",
        },
        {
            "icon": "liderazgo",
            "title": "Formación y Liderazgo",
            "body": "Escuelas de liderazgo juvenil y fortalecimiento administrativo de las "
                    "organizaciones que sostienen cada proyecto.",
            "link_label": "Conocer el área",
            "link_href": "/programas",
        },
    ],

    "voices": [
        {
            "place": "Perú", "date_label": "18 Ago 2026",
            "title": "Cinco escuelas rurales de Cajamarca abren aula de refuerzo en lectura",
            "body": "El programa llega a 640 estudiantes con material impreso propio y docentes "
                    "formados en la sede regional.",
        },
        {
            "place": "Guatemala", "date_label": "14 Ago 2026",
            "title": "Sololá inaugura su primer sistema comunitario de agua potable",
            "body": "240 familias dejan de recorrer más de dos kilómetros diarios para abastecerse.",
        },
        {
            "place": "Bolivia", "date_label": "09 Ago 2026",
            "title": "Riberalta forma a 45 promotores de salud de comunidades ribereñas",
            "body": "La formación se dictó en español y en tacana, con acompañamiento de la "
                    "autoridad indígena local.",
        },
        {
            "place": "Paraguay", "date_label": "03 Ago 2026",
            "title": "Encarnación cierra la sexta cohorte de la Escuela de Liderazgo",
            "body": "Ochenta y dos jóvenes presentaron proyectos propios ante sus municipios.",
        },
        {
            "place": "Ecuador", "date_label": "28 Jul 2026",
            "title": "Convenio con seis municipios de la sierra centro",
            "body": "Permitirá cofinanciar obras de saneamiento durante los próximos tres años.",
        },
        {
            "place": "Honduras", "date_label": "21 Jul 2026",
            "title": "La red de bibliotecas comunitarias suma su sede número treinta",
            "body": "Cada sede es gestionada por un comité de vecinos con presupuesto propio.",
        },
    ],

    "counters": [
        {"number": "1 284", "label": "Proyectos acompañados en 28 territorios"},
        {"number": "47 630", "label": "Personas participantes en programas de formación"},
        {"number": "312", "label": "Organizaciones locales fortalecidas"},
    ],

    "projects": [
        {
            "area_label": "Educación Comunitaria",
            "title": "Aula multigrado y biblioteca escolar en Santa Rosa",
            "place": "Cajamarca, Perú", "href": "/programas", "tone": "teal",
        },
        {
            "area_label": "Agua y Territorio",
            "title": "Sistema de agua potable para 240 familias",
            "place": "Sololá, Guatemala", "href": "/programas", "tone": "amber",
        },
        {
            "area_label": "Salud Territorial",
            "title": "Centro de atención primaria para comunidades ribereñas",
            "place": "Riberalta, Bolivia", "href": "/programas", "tone": "green",
        },
        {
            "area_label": "Formación y Liderazgo",
            "title": "Séptima cohorte de la Escuela de Liderazgo Juvenil",
            "place": "Encarnación, Paraguay", "href": "/programas", "tone": "plum",
        },
    ],

    "news": [
        {
            "day": "20", "month": "Ago",
            "title": "El Instituto publica el presupuesto abierto de sus 1 284 proyectos",
            "summary": "La base de datos puede consultarse y descargarse por territorio, área y año.",
            "href": "#",
        },
        {
            "day": "11", "month": "Ago",
            "title": "Nueva sede territorial en el nororiente ecuatoriano",
            "summary": "Atenderá a doce municipios que hasta ahora dependían de la oficina central.",
            "href": "#",
        },
        {
            "day": "02", "month": "Ago",
            "title": "Convenio de formación docente con seis universidades públicas",
            "summary": "Los cursos serán gratuitos para docentes de escuelas rurales acompañadas.",
            "href": "#",
        },
    ],

    "events": [
        {
            "day": "14", "month": "Oct",
            "title": "Encuentro Regional de Cooperación 2026",
            "summary": "Cartagena · Cuatro días de trabajo con las veintiocho sedes territoriales.",
            "href": "#",
        },
        {
            "day": "30", "month": "Sep",
            "title": "Cierre de la convocatoria a la Escuela de Liderazgo Juvenil",
            "summary": "Inscripciones en línea para jóvenes de 18 a 29 años de los territorios acompañados.",
            "href": "#",
        },
        {
            "day": "12", "month": "Sep",
            "title": "Seminario abierto: agua, cuencas y gobierno comunitario",
            "summary": "Transmisión en línea con traducción simultánea a quechua y guaraní.",
            "href": "#",
        },
    ],

    "documents": [
        {
            "doc_group": "boletin", "title": "N.º 24 — Julio 2026",
            "meta": "Balance semestral y agenda del Encuentro Regional",
            "size_label": "Descargar (4,9 MB)", "href": "#",
        },
        {
            "doc_group": "boletin", "title": "N.º 23 — Marzo 2026",
            "meta": "Especial: agua y gobierno comunitario",
            "size_label": "Descargar (4,1 MB)", "href": "#",
        },
        {
            "doc_group": "boletin", "title": "N.º 22 — Noviembre 2025",
            "meta": "Resultados de la sexta cohorte de liderazgo",
            "size_label": "Descargar (3,6 MB)", "href": "#",
        },
        {
            "doc_group": "memoria", "title": "Memoria Anual 2025",
            "meta": "Estados financieros auditados incluidos",
            "size_label": "Descargar (9,2 MB)", "href": "#",
        },
        {
            "doc_group": "memoria", "title": "Memoria Anual 2024",
            "meta": "Primer año con presupuesto abierto por proyecto",
            "size_label": "Descargar (8,7 MB)", "href": "#",
        },
        {
            "doc_group": "memoria", "title": "Estatuto institucional",
            "meta": "Texto vigente, revisión de 2023",
            "size_label": "Descargar (1,4 MB)", "href": "#",
        },
    ],

    "founders": [
        {
            "photo": "/static/uploads/jaricot.jpg",
            "name": "Beata Paulina María Jaricot",
            "years": "1799-1862",
            "work": "Propagación de la Fe",
            "work_year": "1822",
            "note": "Sostiene las misiones con la oración y la colecta del DOMUND.",
        },
        {
            "photo": "/static/uploads/forbin-janson.jpg",
            "name": "Mons. Charles-Auguste de Forbin-Janson",
            "years": "1765-1844",
            "work": "Santa Infancia",
            "work_year": "1843",
            "note": "Niños que rezan y ayudan a otros niños: Infancia y Adolescencia Misionera.",
        },
        {
            "photo": "/static/uploads/bigard.jpg",
            "name": "Jeanne Bigard",
            "years": "1859-1934",
            "work": "San Pedro Apóstol",
            "work_year": "1889",
            "note": "Formación de seminaristas y novicias en tierras de misión. "
                    "Sostiene los seminarios de África, Asia y Oceanía.",
        },
        {
            "photo": "/static/uploads/manna.jpg",
            "name": "Beato Paolo Manna",
            "years": "1785-1844",
            "work": "Pontificia Unión Misional",
            "work_year": "1916",
            "note": "El alma de las otras tres Obras. No recoge dinero: forma el corazón "
                    "misionero de sacerdotes, religiosos y laicos.",
        },
    ],

    "footer_links": [
        {"column_key": "institucion", "label": "Quiénes somos", "href": "/quienes-somos"},
        {"column_key": "institucion", "label": "Las cuatro áreas", "href": "/quienes-somos"},
        {"column_key": "institucion", "label": "Sedes territoriales", "href": "/territorio"},
        {"column_key": "institucion", "label": "Equipo directivo", "href": "#"},
        {"column_key": "institucion", "label": "Estatuto", "href": "/documentacion"},
        {"column_key": "programas", "label": "Educación Comunitaria", "href": "/programas"},
        {"column_key": "programas", "label": "Salud Territorial", "href": "/programas"},
        {"column_key": "programas", "label": "Agua y Territorio", "href": "/programas"},
        {"column_key": "programas", "label": "Formación y Liderazgo", "href": "/programas"},
        {"column_key": "programas", "label": "Presupuesto abierto", "href": "/programas"},
        {"column_key": "contacto", "label": "Escríbenos", "href": "#"},
        {"column_key": "contacto", "label": "Trabaja con nosotros", "href": "#"},
        {"column_key": "contacto", "label": "Prensa", "href": "#"},
        {"column_key": "contacto", "label": "Transparencia", "href": "#"},
        {"column_key": "contacto", "label": "Preguntas frecuentes", "href": "#"},
    ],

    "legal_links": [
        {"label": "Aviso legal", "href": "#"},
        {"label": "Política de privacidad", "href": "#"},
        {"label": "Política de cookies", "href": "#"},
        {"label": "Créditos fotográficos", "href": "#"},
    ],
}

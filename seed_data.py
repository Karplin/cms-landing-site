# -*- coding: utf-8 -*-
"""Contenido inicial. Solo se inserta la primera vez que se crea cms.db."""

SEED = {
    "settings": {
        "site_title": "Instituto de Cooperación Regional",
        "brand_name": "Instituto de\nCooperación Regional",
        "brand_sub": "Sedes territoriales",
        "header_login": "Acceso",
        "news_col_title": "Noticias",
        "news_col_link": "Todas",
        "events_col_title": "Eventos",
        "events_col_link": "Todos",
        "docs_col1_title": "Boletines",
        "docs_col1_link": "Leer todos",
        "docs_col2_title": "Documentos institucionales",
        "docs_col2_link": "Ver el archivo",
        "campaign_poster": "/static/uploads/afiche-domund-2026.jpg",
        "campaign_motto": "Sinodalidad, unidos en el Espíritu para anunciar el Evangelio",
        "campaign_date": "Domingo 18 de octubre de 2026",
        "campaign_call": "Oración, sacrificio y ofrenda.",
        "campaign_cta_label": "Descargar el folleto",
        "campaign_cta_href": "/static/uploads/brochure-domund.pdf",
        "footer_about_title": "Sobre las OMP",
        "footer_about_text": "Las Obras Misionales Pontificias (OMP) son el principal instrumento de la "
                             "Iglesia católica para atender las grandes necesidades con las que se "
                             "encuentran los misioneros en su labor de evangelización por todo el mundo.\n"
                             "Ofrecen un constante apoyo espiritual y material para que los misioneros "
                             "puedan anunciar el Evangelio y colaborar en el desarrollo personal y social "
                             "del pueblo en medio del cual realizan su labor.",
        "footer_links_title": "Sitios de interés",
        "footer_contact_title": "Información de contacto",
        "address": "Av. Rómulo Betancourt 1608, Mirador Sur\nSanto Domingo, República Dominicana",
        "phone": "809-482-2524, Ext. 117",
        "email": "omprd03@gmail.com",
        "social_facebook": "",
        "social_instagram": "",
        "social_x": "",
        "social_youtube": "",
        "social_spotify": "",
        "copyright": "© 2026 Obras Misionales Pontificias · República Dominicana. "
                     "Todos los derechos reservados.",
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
        "news": {
            "eyebrow": "Actualidad",
            "title": "Noticias y eventos",
            "subtitle": "",
        },
        "documents": {
            "eyebrow": "Documentación",
            "title": "Documentos institucionales",
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




    "news": [],

    "events": [
        {
            "day": "18", "month": "Oct",
            "title": "DOMUND 2026: Domingo Mundial de las Misiones",
            "summary": "Cien años de la Jornada Misionera Mundial, la colecta más universal de la Iglesia.\n"
                       "Lema: «Sinodalidad, unidos en el Espíritu para anunciar el Evangelio».\n"
                       "Oración, sacrificio y ofrenda.",
            "href": "/domund",
            "photo": "/static/uploads/afiche-domund-2026.jpg",
        },
    ],

    "documents": [
        {
            "doc_group": "memoria", "title": "Estatuto de las Obras Misionales Pontificias",
            "meta": "Versión aprobada · 29 páginas",
            "size_label": "Descargar PDF (428 KB)", "href": "/static/uploads/estatutos-omp.pdf",
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
        {"label": "Obras Misionales Pontificias", "href": "https://www.ppoomm.va/es.html"},
        {"label": "La Santa Sede", "href": "https://www.vatican.va/content/vatican/es.html"},
        {"label": "Conferencia del Episcopado Dominicano", "href": "https://ced.org.do/"},
    ],

    "legal_links": [
        {"label": "Aviso legal", "href": "#"},
        {"label": "Política de privacidad", "href": "#"},
        {"label": "Política de cookies", "href": "#"},
        {"label": "Créditos fotográficos", "href": "#"},
    ],
}

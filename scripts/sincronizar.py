# -*- coding: utf-8 -*-
"""Sincroniza el contenido entre producción (Neon) y la base local (SQLite).

Uso, desde la raíz del proyecto:

    python scripts/sincronizar.py bajar         producción -> local
    python scripts/sincronizar.py subir --si    local -> producción

Lee PROD_DATABASE_URL del archivo .env. «bajar» solo lee de producción.
«subir» sobrescribe el contenido de producción: pide --si para no lanzarlo
por accidente, guarda antes una copia de producción en backups/ y lo hace todo
en una sola transacción (si algo falla, producción queda como estaba).

Qué copia y qué no:

- Todo el contenido (áreas, noticias, proyectos...), las secciones y los
  ajustes: lo local se reemplaza por lo de producción.
- Lo que solo existe en local (por ejemplo, un tipo de contenido nuevo que aún
  no se ha desplegado) se conserva.
- Los usuarios NO se copian: el acceso local sigue siendo el de siempre.
- Antes de tocar nada se guarda una copia de la base local en backups/.
"""

import os
import shutil
import sqlite3
import sys
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

AJUSTES_QUE_NO_SE_COPIAN = {"secret_key"}


def leer_env():
    valores = {}
    ruta = os.path.join(RAIZ, ".env")
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    clave, valor = linea.split("=", 1)
                    valores[clave.strip()] = valor.strip()
    return valores


def preparar_base_local():
    """Crea o migra el esquema local usando la propia aplicación (modo SQLite)."""
    os.environ.pop("DATABASE_URL", None)
    from flask import Flask
    import db as capa

    app = Flask(__name__)
    app.teardown_appcontext(capa.close_db)
    with app.app_context():
        capa.init_db()
    return capa.SQLITE_PATH


def tablas_de_prod(cur):
    cur.execute("SELECT table_name AS t FROM information_schema.tables "
                "WHERE table_schema = 'public'")
    return {fila["t"] for fila in cur.fetchall()}


def columnas_locales(con, tabla):
    return [fila[1] for fila in con.execute("PRAGMA table_info(%s)" % tabla)]


def _a_json(valor):
    """Los binarios (archivos subidos) van en base64 en la copia de seguridad."""
    import base64
    if isinstance(valor, (bytes, memoryview)):
        return {"base64": base64.b64encode(bytes(valor)).decode("ascii")}
    return str(valor)


def _sincronizar_media(nombres_origen, nombres_destino, leer, escribir, borrar):
    """Copia solo los archivos que faltan y quita los que sobran en el destino."""
    faltan = sorted(nombres_origen - nombres_destino)
    sobran = sorted(nombres_destino - nombres_origen)
    for nombre in faltan:
        escribir(leer(nombre))
    for nombre in sobran:
        borrar(nombre)
    return len(faltan), len(sobran)


def bajar():
    url = os.environ.get("PROD_DATABASE_URL") or leer_env().get("PROD_DATABASE_URL")
    if not url:
        sys.exit("Falta PROD_DATABASE_URL en el archivo .env.")

    import psycopg2
    import psycopg2.extras
    from schema import CONTENT_TYPES

    ruta_local = preparar_base_local()

    # Copia de seguridad antes de sobrescribir
    os.makedirs(os.path.join(RAIZ, "backups"), exist_ok=True)
    copia = os.path.join(RAIZ, "backups",
                         "cms-%s.db" % datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(ruta_local, copia)
    print("Copia de la base local: %s" % os.path.relpath(copia, RAIZ))

    prod = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
    prod.set_session(readonly=True)
    cur = prod.cursor()
    en_prod = tablas_de_prod(cur)

    local = sqlite3.connect(ruta_local)

    # --- Contenido ---
    for tabla in CONTENT_TYPES:
        if tabla not in en_prod:
            print("  %-13s solo existe en local: se conserva" % tabla)
            continue
        cur.execute("SELECT * FROM %s ORDER BY id" % tabla)
        filas = cur.fetchall()
        destino = columnas_locales(local, tabla)

        local.execute("DELETE FROM %s" % tabla)
        for fila in filas:
            cols = [c for c in destino if c in fila]
            local.execute(
                "INSERT INTO %s (%s) VALUES (%s)" % (
                    tabla, ", ".join(cols), ", ".join("?" for _ in cols)),
                [fila[c] if fila[c] is not None else "" for c in cols],
            )
        print("  %-13s %d registros" % (tabla, len(filas)))

    # --- Secciones (las que solo están en local se conservan) ---
    cur.execute("SELECT * FROM sections")
    secciones = cur.fetchall()
    for s in secciones:
        local.execute(
            "INSERT INTO sections (key, eyebrow, title, subtitle) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET eyebrow = excluded.eyebrow, "
            "title = excluded.title, subtitle = excluded.subtitle",
            (s["key"], s["eyebrow"], s["title"], s["subtitle"]),
        )
    print("  %-13s %d encabezados" % ("sections", len(secciones)))

    # --- Ajustes ---
    cur.execute("SELECT * FROM settings")
    ajustes = [a for a in cur.fetchall() if a["key"] not in AJUSTES_QUE_NO_SE_COPIAN]
    for a in ajustes:
        local.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (a["key"], a["value"]),
        )
    print("  %-13s %d ajustes" % ("settings", len(ajustes)))

    if "media" in en_prod:
        cur.execute("SELECT name FROM media")
        en_origen = {f["name"] for f in cur.fetchall()}
        en_local = {f[0] for f in local.execute("SELECT name FROM media")}

        def leer(nombre):
            cur.execute("SELECT * FROM media WHERE name = %s", (nombre,))
            return cur.fetchone()

        def escribir(f):
            local.execute("INSERT INTO media (name, content_type, size, data) VALUES (?, ?, ?, ?)",
                          (f["name"], f["content_type"], f["size"], bytes(f["data"])))

        nuevos, quitados = _sincronizar_media(
            en_origen, en_local, leer, escribir,
            lambda n: local.execute("DELETE FROM media WHERE name = ?", (n,)))
        print("  %-13s %d nuevos, %d quitados" % ("media", nuevos, quitados))

    print("  %-13s no se copian (el acceso local no cambia)" % "users")

    local.commit()
    local.close()
    prod.close()
    print("Listo: la base local tiene el contenido de producción.")


def migrar_prod(url):
    """Crea y migra el esquema de producción con la misma lógica que la app."""
    import subprocess
    entorno = dict(os.environ, DATABASE_URL=url)
    codigo = ("from flask import Flask; import db; a = Flask('m'); "
              "a.teardown_appcontext(db.close_db)\n"
              "with a.app_context(): db.init_db()")
    subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, env=entorno, check=True)


def subir():
    url = os.environ.get("PROD_DATABASE_URL") or leer_env().get("PROD_DATABASE_URL")
    if not url:
        sys.exit("Falta PROD_DATABASE_URL en el archivo .env.")

    import json
    import psycopg2
    import psycopg2.extras
    from schema import CONTENT_TYPES

    ruta_local = preparar_base_local()
    local = sqlite3.connect(ruta_local)
    local.row_factory = sqlite3.Row

    # 1. Copia de producción antes de tocar nada
    prod = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = prod.cursor()
    copia = {}
    for tabla in sorted(tablas_de_prod(cur)):
        if tabla == "users":
            continue
        cur.execute("SELECT * FROM %s" % tabla)
        copia[tabla] = [dict(f) for f in cur.fetchall()]
    prod.close()
    os.makedirs(os.path.join(RAIZ, "backups"), exist_ok=True)
    ruta_copia = os.path.join(RAIZ, "backups", "prod-%s.json" %
                              datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(ruta_copia, "w", encoding="utf-8") as f:
        json.dump(copia, f, ensure_ascii=False, indent=1, default=_a_json)
    print("Copia de producción: %s" % os.path.relpath(ruta_copia, RAIZ), flush=True)

    # 2. Esquema al día (columnas y tablas nuevas)
    migrar_prod(url)

    # 3. Contenido, en una transacción
    prod = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = prod.cursor()
    try:
        for tabla in CONTENT_TYPES:
            filas = local.execute("SELECT * FROM %s ORDER BY id" % tabla).fetchall()
            cur.execute("DELETE FROM %s" % tabla)
            for fila in filas:
                cols = list(fila.keys())
                cur.execute("INSERT INTO %s (%s) VALUES (%s)" % (
                    tabla, ", ".join(cols), ", ".join("%s" for _ in cols)),
                    [fila[c] for c in cols])
            # Tras insertar ids explícitos, el contador SERIAL debe ir por detrás
            cur.execute("SELECT setval(pg_get_serial_sequence(%s, 'id'), "
                        "COALESCE((SELECT MAX(id) FROM " + tabla + "), 0) + 1, false)",
                        (tabla,))
            print("  %-13s %d registros" % (tabla, len(filas)))

        secciones = local.execute("SELECT * FROM sections").fetchall()
        for s in secciones:
            cur.execute(
                "INSERT INTO sections (key, eyebrow, title, subtitle) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (key) DO UPDATE SET eyebrow = EXCLUDED.eyebrow, "
                "title = EXCLUDED.title, subtitle = EXCLUDED.subtitle",
                (s["key"], s["eyebrow"], s["title"], s["subtitle"]))
        print("  %-13s %d encabezados" % ("sections", len(secciones)))

        ajustes = [a for a in local.execute("SELECT * FROM settings").fetchall()
                   if a["key"] not in AJUSTES_QUE_NO_SE_COPIAN]
        for a in ajustes:
            cur.execute(
                "INSERT INTO settings (key, value) VALUES (%s, %s) "
                "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                (a["key"], a["value"]))
        print("  %-13s %d ajustes" % ("settings", len(ajustes)))

        cur.execute("SELECT name FROM media")
        en_prod_media = {f["name"] for f in cur.fetchall()}
        en_local = {f[0] for f in local.execute("SELECT name FROM media")}

        def escribir(f):
            cur.execute("INSERT INTO media (name, content_type, size, data) VALUES (%s, %s, %s, %s)",
                        (f["name"], f["content_type"], f["size"], psycopg2.Binary(f["data"])))

        nuevos, quitados = _sincronizar_media(
            en_local, en_prod_media,
            lambda n: local.execute("SELECT * FROM media WHERE name = ?", (n,)).fetchone(),
            escribir,
            lambda n: cur.execute("DELETE FROM media WHERE name = %s", (n,)))
        print("  %-13s %d nuevos, %d quitados" % ("media", nuevos, quitados))
        print("  %-13s no se tocan" % "users")

        prod.commit()
    except Exception:
        prod.rollback()
        print("Error: no se ha cambiado nada en producción.")
        raise
    finally:
        prod.close()
        local.close()
    print("Listo: producción tiene el contenido local.")


if __name__ == "__main__":
    orden = sys.argv[1:]
    if orden == ["bajar"]:
        bajar()
    elif orden == ["subir", "--si"]:
        subir()
    else:
        sys.exit(__doc__)

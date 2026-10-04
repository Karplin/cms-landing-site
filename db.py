# -*- coding: utf-8 -*-
"""Acceso a la base de datos.

Funciona sobre PostgreSQL cuando hay DATABASE_URL (el caso de Docker) y sobre
SQLite cuando no la hay (desarrollo local sin contenedores). Las consultas se
escriben una sola vez con marcadores `?` y aquí se traducen al dialecto que
toque; todas las lecturas devuelven diccionarios, así que las plantillas y el
panel no saben cuál de los dos motores hay debajo.
"""

import os
import sqlite3
import time

from flask import g

from schema import CONTENT_TYPES, SECTION_FIELDS, SECTION_KEYS, settings_fields
from seed_data import SEED

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
SQLITE_PATH = os.environ.get("CMS_DB_PATH", os.path.join(BASE_DIR, "cms.db"))

USING_POSTGRES = bool(DATABASE_URL)

_SQL_TYPES = {"number": "INTEGER", "checkbox": "INTEGER"}
_SERIAL = "id SERIAL PRIMARY KEY" if USING_POSTGRES else "id INTEGER PRIMARY KEY AUTOINCREMENT"


# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------

def _connect():
    if USING_POSTGRES:
        import psycopg2
        import psycopg2.extras
        return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)

    conexion = sqlite3.connect(SQLITE_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def get_db():
    if "db" not in g:
        g.db = _connect()
    return g.db


def close_db(exc=None):
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


def esperar_base_de_datos(intentos=30, espera=2):
    """Reintenta la conexión mientras el contenedor de Postgres arranca."""
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            conexion = _connect()
            conexion.close()
            return
        except Exception as error:            # el driver varía según el motor
            ultimo_error = error
            print("Base de datos no disponible (intento %d/%d): %s" % (intento, intentos, error))
            time.sleep(espera)
    raise RuntimeError("No se pudo conectar a la base de datos: %s" % ultimo_error)


# ---------------------------------------------------------------------------
# Ejecución de consultas
# ---------------------------------------------------------------------------

def _dialecto(sql):
    return sql.replace("?", "%s") if USING_POSTGRES else sql


def consultar(sql, params=()):
    """Devuelve todas las filas como diccionarios."""
    cursor = get_db().cursor()
    cursor.execute(_dialecto(sql), tuple(params))
    filas = cursor.fetchall()
    cursor.close()
    return [dict(fila) for fila in filas]


def consultar_una(sql, params=()):
    filas = consultar(sql, params)
    return filas[0] if filas else None


def ejecutar(sql, params=(), commit=True):
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute(_dialecto(sql), tuple(params))
    cursor.close()
    if commit:
        conexion.commit()


def confirmar():
    get_db().commit()


# ---------------------------------------------------------------------------
# Esquema
# ---------------------------------------------------------------------------

def _create_sql(table, fields):
    columnas = [
        _SERIAL,
        "position INTEGER NOT NULL DEFAULT 0",
        "published INTEGER NOT NULL DEFAULT 1",
    ]
    for campo in fields:
        tipo = _SQL_TYPES.get(campo["type"], "TEXT")
        columnas.append("{} {} NOT NULL DEFAULT ''".format(campo["name"], tipo))
    return "CREATE TABLE IF NOT EXISTS {} ({})".format(table, ", ".join(columnas))


# Identificador arbitrario del candado de arranque en Postgres.
_LLAVE_ARRANQUE = 727401


def _tomar_candado():
    """Serializa el arranque: varios procesos pueden crear el esquema a la vez."""
    if USING_POSTGRES:
        ejecutar("SELECT pg_advisory_lock(%d)" % _LLAVE_ARRANQUE, commit=False)


def _soltar_candado():
    if USING_POSTGRES:
        ejecutar("SELECT pg_advisory_unlock(%d)" % _LLAVE_ARRANQUE, commit=False)


def init_db():
    """Crea las tablas que falten y siembra el contenido inicial una sola vez."""
    _tomar_candado()
    try:
        _crear_y_sembrar()
    finally:
        _soltar_candado()


def _columnas_existentes(tabla):
    if USING_POSTGRES:
        filas = consultar(
            "SELECT column_name AS c FROM information_schema.columns "
            "WHERE table_schema = 'public' AND table_name = ?", (tabla,))
        return {f["c"] for f in filas}
    return {f["name"] for f in consultar("PRAGMA table_info(%s)" % tabla)}


def _migrar_columnas(tabla, fields):
    """Añade las columnas que el esquema define y la tabla aún no tiene.

    CREATE TABLE IF NOT EXISTS no altera tablas existentes: sin esto, un campo
    nuevo en schema.py rompería el guardado en una base ya creada.
    """
    existentes = _columnas_existentes(tabla)
    for campo in fields:
        if campo["name"] not in existentes:
            tipo = _SQL_TYPES.get(campo["type"], "TEXT")
            ejecutar("ALTER TABLE {} ADD COLUMN {} {} NOT NULL DEFAULT ''".format(
                tabla, campo["name"], tipo), commit=False)
            print("Migración: %s.%s añadida" % (tabla, campo["name"]))


def _crear_y_sembrar():
    for tabla, spec in CONTENT_TYPES.items():
        ejecutar(_create_sql(tabla, spec["fields"]), commit=False)
        _migrar_columnas(tabla, spec["fields"])

    ejecutar(
        "CREATE TABLE IF NOT EXISTS sections ("
        " key TEXT PRIMARY KEY,"
        " eyebrow TEXT NOT NULL DEFAULT '',"
        " title TEXT NOT NULL DEFAULT '',"
        " subtitle TEXT NOT NULL DEFAULT '')",
        commit=False,
    )
    ejecutar(
        "CREATE TABLE IF NOT EXISTS settings ("
        " key TEXT PRIMARY KEY,"
        " value TEXT NOT NULL DEFAULT '')",
        commit=False,
    )
    ejecutar(
        "CREATE TABLE IF NOT EXISTS users ("
        " {},"
        " username TEXT NOT NULL UNIQUE,"
        " name TEXT NOT NULL DEFAULT '',"
        " password_hash TEXT NOT NULL,"
        " role TEXT NOT NULL DEFAULT 'admin',"
        " active INTEGER NOT NULL DEFAULT 1)".format(_SERIAL),
        commit=False,
    )
    confirmar()

    _sembrar_si_esta_vacio()


def _sembrar_si_esta_vacio():
    for tabla in CONTENT_TYPES:
        if count_rows(tabla):
            continue
        for posicion, fila in enumerate(SEED.get(tabla, []), start=1):
            create(tabla, fila, position=posicion, commit=False)

    for clave, _etiqueta in SECTION_KEYS:
        existe = consultar_una("SELECT 1 AS x FROM sections WHERE key = ?", (clave,))
        if not existe:
            valores = SEED["sections"].get(clave, {})
            ejecutar(
                "INSERT INTO sections (key, eyebrow, title, subtitle) VALUES (?, ?, ?, ?)",
                (clave, valores.get("eyebrow", ""), valores.get("title", ""),
                 valores.get("subtitle", "")),
                commit=False,
            )

    for campo in settings_fields():
        clave = campo["name"]
        existe = consultar_una("SELECT 1 AS x FROM settings WHERE key = ?", (clave,))
        if not existe:
            ejecutar(
                "INSERT INTO settings (key, value) VALUES (?, ?)",
                (clave, SEED["settings"].get(clave, campo.get("default", ""))),
                commit=False,
            )

    confirmar()


# ---------------------------------------------------------------------------
# CRUD genérico de contenido
# ---------------------------------------------------------------------------

def field_names(table):
    return [campo["name"] for campo in CONTENT_TYPES[table]["fields"]]


def list_rows(table, only_published=False):
    sql = "SELECT * FROM {}".format(table)
    if only_published:
        sql += " WHERE published = 1"
    sql += " ORDER BY position ASC, id ASC"
    return consultar(sql)


def rows_by(table, column, value, only_published=True):
    sql = "SELECT * FROM {} WHERE {} = ?".format(table, column)
    if only_published:
        sql += " AND published = 1"
    sql += " ORDER BY position ASC, id ASC"
    return consultar(sql, (value,))


def get_row(table, row_id):
    return consultar_una("SELECT * FROM {} WHERE id = ?".format(table), (row_id,))


def create(table, values, position=None, published=1, commit=True):
    nombres = field_names(table)
    if position is None:
        fila = consultar_una("SELECT COALESCE(MAX(position), 0) AS p FROM {}".format(table))
        position = (fila["p"] or 0) + 1

    columnas = ["position", "published"] + nombres
    params = [position, published] + [values.get(nombre, "") for nombre in nombres]
    ejecutar(
        "INSERT INTO {} ({}) VALUES ({})".format(
            table, ", ".join(columnas), ", ".join("?" for _ in columnas)
        ),
        params,
        commit=commit,
    )


def update(table, row_id, values, published=None):
    nombres = field_names(table)
    asignaciones = ["{} = ?".format(nombre) for nombre in nombres]
    params = [values.get(nombre, "") for nombre in nombres]
    if published is not None:
        asignaciones.append("published = ?")
        params.append(published)
    params.append(row_id)
    ejecutar("UPDATE {} SET {} WHERE id = ?".format(table, ", ".join(asignaciones)), params)


def delete(table, row_id):
    ejecutar("DELETE FROM {} WHERE id = ?".format(table), (row_id,))


def toggle_published(table, row_id):
    ejecutar(
        "UPDATE {} SET published = CASE published WHEN 1 THEN 0 ELSE 1 END "
        "WHERE id = ?".format(table),
        (row_id,),
    )


def move(table, row_id, direction):
    """Intercambia la posición con el registro vecino ('up' o 'down')."""
    filas = list_rows(table)
    indice = next((i for i, fila in enumerate(filas) if fila["id"] == row_id), None)
    if indice is None:
        return
    vecino = indice - 1 if direction == "up" else indice + 1
    if vecino < 0 or vecino >= len(filas):
        return

    for posicion, fila in enumerate(filas, start=1):
        ejecutar("UPDATE {} SET position = ? WHERE id = ?".format(table),
                 (posicion, fila["id"]), commit=False)
    a, b = filas[indice], filas[vecino]
    ejecutar("UPDATE {} SET position = ? WHERE id = ?".format(table),
             (vecino + 1, a["id"]), commit=False)
    ejecutar("UPDATE {} SET position = ? WHERE id = ?".format(table),
             (indice + 1, b["id"]), commit=False)
    confirmar()


def count_rows(table):
    return consultar_una("SELECT COUNT(*) AS n FROM {}".format(table))["n"]


# ---------------------------------------------------------------------------
# Secciones y ajustes
# ---------------------------------------------------------------------------

def all_sections():
    return {fila["key"]: fila for fila in consultar("SELECT * FROM sections")}


def save_sections(payload):
    """payload: {clave_seccion: {campo: valor}}. Solo toca los campos recibidos."""
    validos = {campo["name"] for campo in SECTION_FIELDS}
    for clave, valores in payload.items():
        nombres = [nombre for nombre in valores if nombre in validos]
        if not nombres:
            continue
        ejecutar(
            "UPDATE sections SET {} WHERE key = ?".format(
                ", ".join("{} = ?".format(nombre) for nombre in nombres)
            ),
            [valores[nombre] for nombre in nombres] + [clave],
            commit=False,
        )
    confirmar()


def all_settings():
    return {fila["key"]: fila["value"] for fila in consultar("SELECT * FROM settings")}


def get_setting(key, default=""):
    fila = consultar_una("SELECT value FROM settings WHERE key = ?", (key,))
    return fila["value"] if fila else default


def set_setting(key, value):
    ejecutar(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        (key, value),
    )


def save_settings(values):
    for clave, valor in values.items():
        ejecutar(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
            (clave, valor),
            commit=False,
        )
    confirmar()


# ---------------------------------------------------------------------------
# Usuarios
# ---------------------------------------------------------------------------

def list_users():
    return consultar("SELECT * FROM users ORDER BY username ASC")


def get_user(user_id):
    return consultar_una("SELECT * FROM users WHERE id = ?", (user_id,))


def get_user_by_username(username):
    return consultar_una("SELECT * FROM users WHERE username = ?", (username,))


def count_users(only_active=False):
    sql = "SELECT COUNT(*) AS n FROM users"
    if only_active:
        sql += " WHERE active = 1"
    return consultar_una(sql)["n"]


def ensure_initial_user(username, name, password_hash):
    """Crea el primer usuario si la tabla está vacía. Seguro con varios procesos."""
    _tomar_candado()
    try:
        if count_users():
            return False
        create_user(username, name, password_hash)
        return True
    finally:
        _soltar_candado()


def create_user(username, name, password_hash, role="admin", active=1):
    ejecutar(
        "INSERT INTO users (username, name, password_hash, role, active) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, name, password_hash, role, active),
    )


def update_user(user_id, username, name, role, active):
    ejecutar(
        "UPDATE users SET username = ?, name = ?, role = ?, active = ? WHERE id = ?",
        (username, name, role, active, user_id),
    )


def set_user_password(user_id, password_hash):
    ejecutar("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))


def delete_user(user_id):
    ejecutar("DELETE FROM users WHERE id = ?", (user_id,))

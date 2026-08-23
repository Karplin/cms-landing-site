FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Las dependencias primero: así la capa se reutiliza mientras no cambien.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Sin privilegios de root dentro del contenedor.
RUN useradd --create-home --uid 1000 cms && chown -R cms:cms /app
USER cms

EXPOSE 8000

# 3 procesos; el arranque espera a Postgres y siembra la base si hace falta.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", \
     "--preload", "app:app"]

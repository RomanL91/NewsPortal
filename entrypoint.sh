#!/bin/sh
set -e

echo "[*] Running makemigrations..."
python manage.py makemigrations

echo "[*] Running migrate..."
python manage.py migrate

echo "[*] Collecting static files..."
python manage.py collectstatic --no-input

echo "[*] Compiling translations..."
django-admin compilemessages -l ru --ignore=*.venv/* || echo "compilemessages failed"

echo "[*] Starting server..."
exec uvicorn core.asgi:application --host 0.0.0.0 --port 9999

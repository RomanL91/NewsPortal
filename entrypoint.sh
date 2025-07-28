CRLFcrlf#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

uvicorn core.asgi:application --host 0.0.0.0 --port 9999
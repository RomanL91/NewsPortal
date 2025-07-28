FROM python:3.11.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка зависимостей ОС (включая gettext для compilemessages)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    gettext \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    bash

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

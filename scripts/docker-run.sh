#!/bin/sh
set -e

python manage.py migrate
gunicorn -b :8000 --chdir /app app.wsgi:application
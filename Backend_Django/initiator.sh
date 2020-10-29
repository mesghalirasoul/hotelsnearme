#!/bin/sh

echo "Running migration scripts..."
poetry run python manage.py migrate

echo "Starting application..."

poetry run python manage.py runserver 0.0.0.0:${PORT}

#gunicorn --bind 0.0.0.0:8000 aiml_api.wsgi:application

#!/bin/bash
## SET SUPERUSER EMAIL
export SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'none'}

cd /app/
## MIGRATE DATABASE
/opt/venv/bin/python manage.py migrate --noinput


## CREATE DJANGOSUPERUSER
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
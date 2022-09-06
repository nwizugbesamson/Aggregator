#!/bin/bash
## SET SUPERUSER EMAIL
export SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'none'}
export SUPERUSER=${DJANGO_SUPERUSER}
export SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD}

cd /app/



## CHECK IF DB IS AVAILABLE BEFORE CONNECTION OR MIGRATION
## MIGRATE DATABASE
/opt/venv/bin/python manage.py wait_for_db

/opt/venv/bin/python manage.py makemigrations 
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py collectstatic --noinput

/opt/venv/bin/python manage.py crontab add






## CREATE DJANGOSUPERUSER
# /opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --password $SUPERUSER_PASSWORD  --username $SUPERUSER --noinput  || true
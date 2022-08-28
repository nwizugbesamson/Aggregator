#!/bin/bash
## SET SUPERUSER EMAIL
SUPERUSER_EMAIL = ${DJANGO_SUPERUSER_EMAIL:-'none'}

cd /app/
## MIGRATE DATABASE
/opt/venv/bin/python main.py migrate


## CREATE DJANGOSUPERUSER
/opt/venv/bin/python main createsuperuser --email $SUPERUSER_EMAIL --noinput || true
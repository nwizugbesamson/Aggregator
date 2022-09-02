#!/bin/bash

# export APP_PORT=${PORT:-8000}
cd /app/

# /opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm web_service.wsgi:application --bind '0.0.0.0:'${APP_PORT}
/opt/venv/bin/uwsgi --socket :9000 --workers 4 --master --enable-threads --module web_service.wsgi


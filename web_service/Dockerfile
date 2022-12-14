# python version
FROM python:3.10.6-slim

USER root

# copy all files into docker directory app
COPY ./requirements.txt /app/requirements.txt



# virtual env within the /opt/ directory
RUN python3 -m venv /opt/venv

## upgrade pip to latest version
## install requirements.txt
## create user app
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd && \
    apt-get install -y libxml2-dev libxslt1-dev python-dev libpython3-dev \
        libpcre3 libpcre3-dev  uwsgi-plugin-python3 python3-all-dev && \
    apt-get install -y install cron &&\
    apt-get install -y gcc  python3-setuptools  &&\
    /opt/venv/bin/pip install -U pip &&\
    /opt/venv/bin/pip cache purge &&\
    /opt/venv/bin/pip install wheel &&\
    /opt/venv/bin/pip install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz &&\
    /opt/venv/bin/pip install -r /app/requirements.txt &&\
    /opt/venv/bin/python -c "import nltk; nltk.download('punkt', download_dir='/opt/venv/lib/nltk_data')" &&\
    /opt/venv/bin/python -c "import nltk; nltk.download('stopwords', download_dir='/opt/venv/lib/nltk_data')" &&\
    apt-get clean &&\
    adduser --disabled-password --no-create-home samson &&\
    mkdir -p /app/vol/web/static && \
    # chown -R samson:samson /app/vol/web/static && \
    chmod -R 755 /app/vol/web/static && \
    # chown -R samson:samson /opt/venv/lib/python3.10/site-packages/django_plotly_dash/migrations/ &&\
    chmod -R 777 /opt/venv/lib/python3.10/site-packages/django_plotly_dash/migrations/ &&\
    touch /var/log/cron.log
    
# copy all files into docker directory app
COPY . /app

# designate app directory as working directory
WORKDIR /app

## allow execution on entrypoint.sh file
RUN chmod +x entrypoint.sh &&\
    chmod +x /app/migrate.sh 
    # chown -R samson:samson /app/*/migrations && \
    # chmod -R 777 /app/*/migrations 

## change user to app user created above
# USER samson


# ## docker start command
# CMD ["/app/entrypoint.sh"]
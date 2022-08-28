# python version
FROM python:3.10.6

# copy all files into docker directory app
COPY . /app

# designate app directory as working directory
WORKDIR /app

# virtual env within the /opt/ directory
RUN python3 -m venv /opt/venv

## upgrade pip to latest version
## install requirements.txt
RUN /opt/venv/bin/pip install -U pip && \
    /opt/venv/bin/pip install -r requirements.txt

## allow execution on entrypoint.sh file
RUN chmod +x entrypoint.sh

## docker start command
CMD ["/app/entrypoint.sh"]
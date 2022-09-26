FROM python:3.10-slim

RUN apt update && apt install curl -y

COPY shop/requirements.txt /requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt

COPY wait-for-command.sh /

COPY shop app/

WORKDIR app/

EXPOSE 5001

RUN chmod +x docker-entrypoint.sh /wait-for-command.sh run.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ['python', 'wsgi.py']
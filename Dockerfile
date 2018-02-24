FROM ubuntu:latest

ENV MYSQL_USER=root \
    MYSQL_PASSWORD= \
    MYSQL_DATABASE=cs5331

RUN apt-get update \
    && apt-get install -y python-pip \
    && apt-get install -y apache2 \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

RUN pip install -U pip flask flask-cors \
    && pip install --upgrade pip

ADD ./src/service /service
#ADD ./src/html /var/www/html

CMD ["/bin/bash", "/service/start_services.sh"]

EXPOSE 8080
EXPOSE 80



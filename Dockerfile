FROM ubuntu:latest

ENV MYSQL_USER=root \
    MYSQL_PASSWORD= \
    MYSQL_HOST=localhost \
    MYSQL_DATABASE=cs5331

RUN apt-get update \
    && apt-get install -y python-pip \
    && apt-get install -y apache2 \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server \
    && apt-get install -y libmysqlclient-dev

RUN pip install -U pip flask flask-cors Flask-SQLAlchemy MySQL-python

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN echo "$user    hard    nproc    20" >> /etc/security/limits.conf

ADD ./src/service /service
ADD ./src/html /var/www/html

EXPOSE 80
EXPOSE 8080

CMD ["/bin/bash", "/service/start_services.sh"]

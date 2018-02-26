FROM ubuntu:latest

ENV MYSQL_USER=root \
    MYSQL_PASSWORD= \
    MYSQL_HOST=localhost \
    MYSQL_DATABASE=GROUP5_SECRET_DIARY

RUN apt-get update \
    && apt-get install -y python-pip \
    && apt-get install -y apache2

ADD ./src/db /tmp/

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server && \
    rm -rf /var/lib/apt/lists/* && \
    sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/my.cnf && \
    sed -i 's/^\(log_error\s.*\)/# \1/' /etc/mysql/my.cnf && \
    service mysql start && \
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS GROUP5_SECRET_DIARY CHARACTER SET utf8 COLLATE utf8_general_ci; FLUSH PRIVILEGES;" && \
    mysql -u root -e "SHOW DATABASES" && \
    mysql -u root "GROUP5_SECRET_DIARY" < "/tmp/schema.sql"

RUN mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld
VOLUME ["/etc/mysql", "/var/lib/mysql"]
WORKDIR /data

RUN apt-get update && \
    apt-get install -y libmysqlclient-dev

RUN pip install -U pip flask flask-cors Flask-SQLAlchemy MySQL-python flask-bcrypt

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN echo "$user    hard    nproc    20" >> /etc/security/limits.conf

ADD ./src/service /service
ADD ./src/html /var/www/html

EXPOSE 80
EXPOSE 8080
EXPOSE 3306

CMD ["/bin/bash", "/service/start_services.sh"]

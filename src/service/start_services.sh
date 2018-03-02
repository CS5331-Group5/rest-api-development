#!/bin/bash

service mysql start

apachectl start

sleep 3

service mysql status

mysql -u root -e "USE GROUP5_SECRET_DIARY; SHOW TABLES"

python /service/app.py

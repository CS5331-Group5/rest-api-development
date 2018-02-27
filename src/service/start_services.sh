#!/bin/bash

service mysql start

apachectl start

sleep 3

service mysql status

mysql -u root "GROUP5_SECRET_DIARY" < "/service/populate.sql"
mysql -u root -e "USE GROUP5_SECRET_DIARY; SHOW TABLES"

python /service/app.py

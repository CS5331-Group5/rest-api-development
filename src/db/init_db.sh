#!/bin/bash

service mysql start

sleep 3

mysql -u root -e "CREATE DATABASE IF NOT EXISTS GROUP5_SECRET_DIARY CHARACTER SET utf8 COLLATE utf8_general_ci; FLUSH PRIVILEGES;"
mysql -u root -e "SHOW DATABASES"
mysql -u root "GROUP5_SECRET_DIARY" < "/tmp/schema.sql"
mysql -u root -e "USE GROUP5_SECRET_DIARY; SHOW TABLES"
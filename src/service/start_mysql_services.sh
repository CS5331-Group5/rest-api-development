#!/bin/bash

service mysql start

apachectl start

sleep 3

service mysql status

mysql -u root -e "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\` CHARACTER SET utf8 COLLATE utf8_general_ci; FLUSH PRIVILEGES;"
mysql -u root -e "SHOW DATABASES"

mysql -u root "$MYSQL_DATABASE" < "/service/schema.sql"
mysql -u root -e "USE \`$MYSQL_DATABASE\`; SHOW TABLES"

python /service/app.py

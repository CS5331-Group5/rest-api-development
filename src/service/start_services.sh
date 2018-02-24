#!/bin/bash

cd /service/
pip install django
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8080


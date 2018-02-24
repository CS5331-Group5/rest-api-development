#!/bin/bash

#pip install -r requirements.txt
#python manage.py makemigrations

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
python manage.py migrate --noinput
fi


#!/bin/bash

sleep 15
cd /usr/src/app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --noreload

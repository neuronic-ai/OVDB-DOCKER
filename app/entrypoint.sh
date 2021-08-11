#!/bin/bash

cd /usr/src/app
python mange.py makemigrations
python mange.py migrate
python manage.py runserver 0.0.0.0:8000 --noreload

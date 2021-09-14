#!/bin/bash

sleep 30
cd /usr/src/api
python manage.py makemigrations
python manage.py runserver 0.0.0.0:8001 --noreload

#!/bin/bash

sleep 30
cd /usr/src/app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --noreload

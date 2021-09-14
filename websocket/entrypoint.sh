#!/bin/bash

sleep 30
cd /usr/src/websocket
python manage.py makemigrations
python manage.py runserver 0.0.0.0:8002 --noreload

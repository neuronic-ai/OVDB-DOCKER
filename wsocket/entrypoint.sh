#!/bin/bash

cd /usr/src/wsocket
python manage.py runserver 0.0.0.0:8000 --noreload

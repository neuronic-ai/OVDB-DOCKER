#!/bin/bash

cd /usr/src/app
python manage.py runserver 0.0.0.0:8000 --noreload

#!/bin/bash

sleep 30
cd /usr/src/webhook
python manage.py runserver 0.0.0.0:8002 --noreload

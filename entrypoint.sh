#!/bin/bash

python manage.py migrate
granian \
    --interface asgi \
    --host 0.0.0.0 \
    --static-path-route /static \
    --static-path-mount /app/static \
    --static-path-route /media \
    --static-path-mount /app/media \
    config.asgi:application

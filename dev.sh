#!/bin/bash

./install-tailwind.sh
./tailwindcss -i ./styles.css -o ./static/css/main.css -m
DEBUG=1 python manage.py runserver

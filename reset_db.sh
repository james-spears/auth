#!/bin/bash

su - postgres -c "dropdb postgres"

su - postgres -c "createdb postgres"

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

source /home/james/.profile
/home/james/.pyenv/shims/python manage.py makemigrations
/home/james/.pyenv/shims/python manage.py migrate

export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="admin@example.com"
export DJANGO_SUPERUSER_PASSWORD="@ABC123xyz"
/home/james/.pyenv/shims/python manage.py createsuperuser --no-input

/home/james/.pyenv/shims/python manage.py shell < seed.py

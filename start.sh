#!/bin/bash

ARG=$1

RUN_MODE=${ARG:-"app"};

case ${RUN_MODE} in
    "app")
        ./install-tailwind.sh
        ./tailwindcss -i ./styles.css -o ./static/css/main.css -m
        python manage.py collectstatic --noinput
        find /var/www/fastinvites.com -type d -exec chmod 755 {} \;
        find /var/www/fastinvites.com -type f -exec chmod 644 {} \;
        gunicorn -b 0.0.0.0:8000 app.wsgi
        # python manage.py runserver 0.0.0.0:8000
        ;;
    "worker")
        celery -A app worker --loglevel=info
        ;;
    "monitor")
        celery -A app flower
        ;;
    *)
        echo "Unknown run mode. Doing nothing."
        exit 1;
        ;;
esac

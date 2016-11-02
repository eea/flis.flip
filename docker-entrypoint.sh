#!/usr/bin/env bash

crontab ./crontab.cfg
cron
./manage.py migrate --fake-initial
./manage.py loadfixtures
./manage.py load_metadata_fixtures
./manage.py collectstatic --noinput
gunicorn flip.wsgi:application --bind 0.0.0.0:8001

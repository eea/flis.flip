#!/usr/bin/env bash

./manage.py migrate
./manage.py loadfixtures
./manage.py load_metadata_fixtures
./manage.py collectstatic --noinput
gunicorn flip.wsgi:application --bind 0.0.0.0:8001

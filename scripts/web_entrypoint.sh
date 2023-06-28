#!/bin/bash

python manage.py migrate

python manage.py collectstatic --noinput

if [[ $ENVIRONMENT == "dev" ]]
then
    echo "--> Starting development server."
    python manage.py runserver 0.0.0.0:8000
elif [[ $ENVIRONMENT == "prod" ]]
then
    echo "--> Starting gunicorn server"
    gunicorn config.wsgi:application -w 25 -b 0.0.0.0:8000
fi
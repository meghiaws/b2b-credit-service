#!/bin/bash

E_NO_POSTGRES_USERNAME=60

POSTGRES_USERNAME="$1"
DATABASE_NAME="credit_service"

if [[ -z "$POSTGRES_USERNAME" ]]
then
    echo "Call `basename $0` with your postgres user as the first argument."
    exit "$E_NO_POSTGRES_USERNAME"
fi

dropdb --if-exists "$DATABASE_NAME"

sudo -u postgres createdb -O "$POSTGRES_USER" "$DATABASE_NAME"

python manage.py migrate

python manage.py collectstatic --noinput


if [ "$ENVIRONMENT"="dev" ]
then
    echo "--> Starting development server."
    python manage.py runserver 0.0.0.0:8000
elif ["$ENVIRONMENT"="prod"]
then
    echo "--> Starting gunicorn server"
    gunicorn config.wsgi:application -b 0.0.0.0:8000
fi
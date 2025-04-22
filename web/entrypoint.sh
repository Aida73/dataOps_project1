#!/bin/bash

# This script is used to start the web server and run the database migrations.
# Wait for the database to be ready before running migrations and starting the server.
echo "Waiting for the database to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "PostgreSQL started"
# Apply migrations and start server
python mysite/manage.py makemigrations
python mysite/manage.py migrate
python manage.py create_admin_account
python mysite/manage.py runserver 0.0.0.0:8000
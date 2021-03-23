#!/bin/bash

rm db-dev.sqlite3 db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py refresh_fixtures --profiles=100
rm db-dev.sqlite3 db.sqlite3
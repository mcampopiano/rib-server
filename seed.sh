#!/bin/bash

rm -rf ribapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations ribapi
python3 manage.py migrate ribapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata contractors
python3 manage.py loaddata clients
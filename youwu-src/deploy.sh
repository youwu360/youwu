#!/usr/bin/env bash



rm db.sqlite3
rm site_youwu/migrations/*_initial.py
python3 manage.py makemigrations
python3 manage.py migrate

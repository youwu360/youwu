#!/usr/bin/env bash
set -e

cd $(dirname $0)
path=$(pwd)

if [ -f items.json ]
then
    rm items.json
    fi

unzip items.json.zip

if [ -f db.sqlite3 ]
then
    rm db.sqlite3
    fi
if [ -f site_youwu/migrations/*_initial.py ]
then
    rm site_youwu/migrations/*_initial.py
    fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 load_nvshens_data.py

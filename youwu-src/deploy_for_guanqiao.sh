#!/usr/bin/env bash
set -e

if [ -f ../spider/spider_nvshens/myproject/items.json ]
then
    rm ../spider/spider_nvshens/myproject/items.json
    fi

tar -zxvf items.json.tar.gz -C ../spider/spider_nvshens/myproject/

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

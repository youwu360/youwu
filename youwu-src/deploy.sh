#!/usr/bin/env bash
set -e

cd $(dirname $0)
path=$(pwd)

cd $path/../spider/spider_nvshens/myproject/myproject/
rm items.json
scrapy crawl nvshens -o items.json -t json

cd $path
rm db.sqlite3
rm site_youwu/migrations/*_initial.py

python3 manage.py makemigrations
python3 manage.py migrate
python3 load_nvshens_data.py

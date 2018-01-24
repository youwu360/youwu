#!/usr/bin/env bash

rm items.json
rm log

nohup scrapy crawl nvshens -o items.json -t json 1>./log 2>./log &

#!/usr/bin/env bash

rm items.json
rm log

scrapy crawl nvshens -o items.json -t json 1>./log 2>./log

t=`date +%Y-%m-%d-%H-%M`
cp items.json items.json.${t}
zip items.json.zip.${t} items.json


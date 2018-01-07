
rm items.json

scrapy crawl nvshens -o items.json -t json | out-file log

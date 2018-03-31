1. my_project:
    run_spider, get items.json

2. scrapy_album_image_to_local
    a. collect_album_url.py
        input : items.json
        output:
        res[Constants.starCover] = self.starCover
        res[Constants.albumCover] = self.albumCover
        res[Constants.albumToStar] = self.albumToStar
        res[Constants.albumImageList] = self.albumImageList

    b. scrapy_album_image_to_local.py
        input : all_image_urls.json, allUrlsForProduct.json
        set = all_image_urls.json - allUrlsForProduct.json
        scrapy set

    c. update_seaweedfs.py
        input :
            allStarCover.json : all star cover in one file
            albumInJsonPath : every album have a json file

        output :
            allUrlsForProduct.json

Todo
3. load_nvshen_data.py
    extract star, album, tag data to db
4. load_new_cover.py
    update db's star cover, album cover url to seaweedfs's


Online data organize:
Tables:
    star: star info, and url of star cover(weedfs)
    album: album info, and url of album cover(weedfs)
    tags: tags and it's album id list

album image list:
    in json file(allUrlsForProduct.json),
    load to memory when service starts

import os
import json
import urllib.request
import shutil
import hashlib
import time
import threading
from scrapy_album_image_to_local_helper import ImageDownloadHelper
from scrapy_album_image_to_local_helper import AlbumCoverLoader

image_download_helper = ImageDownloadHelper()
album_cover_loader = AlbumCoverLoader()

basePath = os.path.dirname(os.path.realpath(__file__))
albumImageListFIlePath = "../../../youwu-resource/data/url_info/"


newly_scrapyed_json_file = os.path.join(basePath, "../../../youwu-src/all_image_urls.json")
product_json_file = os.path.join(basePath, "allUrlsForProduct.json")
extra_album_cover_file = os.path.join(basePath, "extra_album_cover_file")

newly_scrapyed_json = image_download_helper.load_file_to_json(newly_scrapyed_json_file)
product_json = image_download_helper.load_file_to_json(product_json_file)
extra_album_cover_json = album_cover_loader.load(extra_album_cover_file)

joined_json = image_download_helper.join_result(newly_scrapyed_json, extra_album_cover_json,
                                                image_download_helper.add)
joined_json = image_download_helper.join_result(joined_json, product_json,
                                                image_download_helper.minus)


for starId in joined_json[image_download_helper.starCover]:
    url = joined_json[image_download_helper.starCover][starId]
    subFolder = "cover/" + image_download_helper.get_hash_code(starId, None)
    subFolderPath = os.path.join(basePath, subFolder)
    if not os.path.exists(subFolderPath):
        os.mkdir(subFolderPath)
    image_download_helper.download_star_cover(subFolderPath, url, starId)
    cnt = threading.active_count()
    print("in albumImageList, cnt: " + str(cnt))
    if (cnt > 5):
        time.sleep(0.3)
    break

for albumId in joined_json[image_download_helper.albumCover]:
    url = joined_json[image_download_helper.albumCover][albumId]
    if albumId in joined_json[image_download_helper.albumToStar]:
        try:
            starId = joined_json[image_download_helper.albumToStar][albumId]
        except:
            print("can not get starId by albumId : " + str(albumId))
            continue
    else:
        print('----------')
        print("albumId is null")
        print(url)
        continue

    subFolder = "data/" + image_download_helper.get_hash_code(starId, albumId)
    subFolderPath = os.path.join(basePath, subFolder)
    if not os.path.exists(subFolderPath):
        os.mkdir(subFolderPath)

    localAlbumDir = os.path.join(subFolderPath, str(starId) + "." + str(albumId))
    if not os.path.exists(localAlbumDir):
        os.mkdir(localAlbumDir)

    image_download_helper.download_album_cover(localAlbumDir, url, starId, albumId)
    cnt = threading.active_count()
    print("in albumImageList, cnt: " + str(cnt))
    if (cnt > 5):
        time.sleep(0.3)

for albumId in joined_json[image_download_helper.albumImageList]:
    try:
        starId = joined_json[image_download_helper.albumToStar][albumId]
    except:
        print("can not get starId by albumId : " + str(albumId))
        continue

    subFolder = "data/" + image_download_helper.get_hash_code(starId, albumId)
    subFolderPath = os.path.join(basePath, subFolder)
    if not os.path.exists(subFolderPath):
        os.mkdir(subFolderPath)

    localAlbumDir = os.path.join(subFolderPath, str(starId) + "." + str(albumId))
    if not os.path.exists(localAlbumDir):
        os.mkdir(localAlbumDir)

    albumDict = joined_json[image_download_helper.albumImageList][albumId]
    for img in albumDict:
        imgUrl = albumDict[img]
        image_download_helper.download_album_image(localAlbumDir, imgUrl, starId, albumId)
        cnt = threading.active_count()
        print("in albumImageList, cnt: " + str(cnt))
        if (cnt > 5):
            time.sleep(0.3)

time.sleep(10)



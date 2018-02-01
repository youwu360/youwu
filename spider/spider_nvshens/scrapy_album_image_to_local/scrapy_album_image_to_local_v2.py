import os
import json
import urllib.request
import shutil
import hashlib
import time
import threading
from scrapy_album_image_to_local_helper import ImageDownloadHelper

image_download_helper = ImageDownloadHelper()


basePath = os.path.dirname(os.path.realpath(__file__))
albumImageListFIlePath = "../../../youwu-resource/data/url_info/"


newly_scrapyed_json_file = os.path.join(basePath, "../../../youwu-src/all_image_urls.json")
failed_json_file = os.path.join(basePath, "failed.json")
product_json_file = os.path.join(basePath, "product.json")


newly_scrapyed_json = image_download_helper.load_file_to_json(newly_scrapyed_json_file)
failed_json = image_download_helper.load_file_to_json(failed_json_file)
product_json = image_download_helper.load_file_to_json(product_json_file)

joined_json = image_download_helper.join_result(newly_scrapyed_json, failed_json,
                                                image_download_helper.add)
joined_json = image_download_helper.join_result(joined_json, product_json,
                                                image_download_helper.minus)


coverUrl = 'https://img.onvshen.com:85/gallery/__sub__/cover/0.jpg'


with open(albumIdFile, 'r') as fp:
    lines = fp.readlines()
    for line in lines:
        if line is None or line == '':
            break
        line = line.strip()
        if line.startswith('#'):
            continue

        arr = line.split('/')
        starId = arr[0]
        albumId = arr[1]

        subFolder = "data/" + image_download_helper.get_hash_code(starId, albumId)
        subFolderPath = os.path.join(basePath, subFolder)
        if not os.path.exists(subFolderPath):
            os.mkdir(subFolderPath)

        localAlbumDir = os.path.join(subFolderPath, str(starId) + "." + str(albumId))
        if not os.path.exists(localAlbumDir):
            os.mkdir(localAlbumDir)

        image_url = coverUrl.replace('__sub__', line)
        image_download_helper.download_album_image(localAlbumDir, image_url, starId, albumId)

        urlFileName = str(starId) + "." + str(albumId)
        albumImageListFile = os.path.join(basePath, albumImageListFIlePath + urlFileName)
        print(os.path.abspath(albumImageListFile))
        with open(albumImageListFile, 'r') as fp:
            imageUrls = json.load(fp)
            for image_url in imageUrls:
                image_download_helper.download_album_image(localAlbumDir, image_url, starId, albumId)
                cnt = threading.active_count()
                print(cnt)
                if (cnt > 3):
                    time.sleep((cnt - 3) / 5.0)



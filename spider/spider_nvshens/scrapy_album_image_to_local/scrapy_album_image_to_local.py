import os
import json
import urllib.request
import shutil
import hashlib
from scrapy_album_image_to_local_helper import get_hash_code

basePath = os.path.dirname(os.path.realpath(__file__))
albumIdFile = os.path.join(basePath, "starAndAlbumId.txt")
albumImageListFIlePath = "../../../youwu-resource/data/url_info/"

coverUrl = "https://img.onvshen.com:85/gallery/__sub__/cover/0.jpg"

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

        subFolder = "test_data/" + get_hash_code(starId, albumId)
        subFolderPath = os.path.join(basePath, subFolder)
        if not os.path.exists(subFolderPath):
            os.mkdir(subFolderPath)

        localAlbumDir = os.path.join(subFolderPath, str(starId) + "." + str(albumId))
        if not os.path.exists(localAlbumDir):
            os.mkdir(localAlbumDir)

        cover = coverUrl.replace('__sub__', line)
        urllib.request.urlretrieve(cover, os.path.join(localAlbumDir, "cover.jpg"))

        urlFileName = str(starId) + "." + str(albumId)
        albumImageListFile = os.path.join(basePath, albumImageListFIlePath + urlFileName)
        print(os.path.abspath(albumImageListFile))
        with open(albumImageListFile, 'r') as fp:
            urls = json.load(fp)
            for url in urls:
                try:
                    arr = url.split('/')
                    img_path = os.path.join(localAlbumDir, arr[-1])
                    if os.path.exists(img_path):
                        print("already exists url : " + url)
                        continue
                    urllib.request.urlretrieve(url, img_path)
                    print("success url : " + url)
                except Exception as e:
                    print("failed url : " + url)
                    print(e)


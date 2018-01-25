import os
import json
import urllib.request
import shutil


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

        localAlbumDir = os.path.join(basePath, "test_data/" + str(starId) + "." + str(albumId))
        if os.path.exists(localAlbumDir):
            shutil.rmtree(localAlbumDir)
        os.mkdir(localAlbumDir)

        cover = coverUrl.replace('__sub__', line)
        urllib.request.urlretrieve(cover, os.path.join(localAlbumDir, "cover.jpg"))

        urlFileName = str(starId) + "." + str(albumId)
        albumImageListFile = os.path.join(basePath, albumImageListFIlePath + urlFileName)
        print(os.path.abspath(albumImageListFile))
        with open(albumImageListFile, 'r') as fp:
            urls = json.load(fp)
            for url in urls:
                arr = url.split('/')
                urllib.request.urlretrieve(url, os.path.join(localAlbumDir, arr[-1]))

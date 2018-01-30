import os
import json
import urllib.request
import shutil
import hashlib
import threading


def get_hash_code(starId, albumId):
    res = hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2]
    return str(res)


def down_load_image_async(localAlbumDir, url):
    t = threading.Thread(target=down_load_image, args=(localAlbumDir, url,))
    t.setDaemon(True)
    t.start()


def down_load_image(localAlbumDir, url):
    try:
        arr = url.split('/')
        img_path = os.path.join(localAlbumDir, arr[-1])
        if os.path.exists(img_path):
            print("already exists url : " + url)
            return
        urllib.request.urlretrieve(url, img_path)
        print("success url : " + url)
    except Exception as e:
        print("failed url : " + url)
        print(e)
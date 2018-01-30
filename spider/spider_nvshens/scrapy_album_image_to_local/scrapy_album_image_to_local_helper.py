import os
import json
import urllib.request
import shutil
import hashlib
import threading


class ImageDownloadHelper(object):
    daolianSize = 4039
    basePath = os.path.dirname(os.path.realpath(__file__))

    coverPatterns = ["https://img.onvshen.com:85/gallery/__sub__/cover/",
                     "https://t1.onvshen.com:85/gallery/__sub__/cover/"]

    imagePatterns = ['https://img.onvshen.com:85/gallery/__sub__/',
                     'https://img.onvshen.com:85/gallery/__sub__/s/',
                     'https://t1.onvshen.com:85/gallery/__sub__/s/',
                     'https://t1.onvshen.com:85/gallery/__sub__/']

    def download_album_cover(self, localAlbumDir, cover_url, starId, albumId):
        self.down_load_image_async(localAlbumDir, cover_url, starId, albumId, self.coverPatterns)

    def download_album_image(self, localAlbumDir, image_url, starId, albumId):
        self.down_load_image_async(localAlbumDir, image_url, starId, albumId, self.imagePatterns)

    def get_hash_code(self, starId, albumId):
        res = hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2]
        return str(res)

    def down_load_image_async(self, localAlbumDir, image_url, starId, albumId, imagePatterns):
        t = threading.Thread(target=self.down_load_image,
            args=(localAlbumDir, image_url, starId, albumId, imagePatterns,))
        t.setDaemon(True)
        t.start()

    def down_load_image(self, localAlbumDir, url, starId, albumId, imagePatterns):
        arr = url.split('/')
        img_path = os.path.join(os.path.join(localAlbumDir, arr[-1]))
        if os.path.exists(img_path):
            fileSize = os.path.getsize(img_path)
            if fileSize != self.daolianSize:
                print("already exists url : " + url)
                return
            else:
                print('daolian file; retry image : ' + url)

        try:
            urllib.request.urlretrieve(url, img_path)
            fileSize = os.path.getsize(img_path)
            if fileSize != self.daolianSize:
                print("success url : " + url)
            else:
                self.down_load_by_pattern(starId, albumId, url, img_path, imagePatterns)
        except:
                self.down_load_by_pattern(starId, albumId, url, img_path, imagePatterns)

    def down_load_by_pattern(self, starId, albumId, url, img_path, imagePatterns):
        success = False
        arr = url.split('/')
        for image_pattern in imagePatterns:
            try:
                new_url = image_pattern.replace('__sub__',
                    str(starId) + "/" + str(albumId)) + arr[-1]
                urllib.request.urlretrieve(new_url, img_path)
                fileSize = os.path.getsize(img_path)
                if fileSize != self.daolianSize:
                    print("success url by pattern : " + image_pattern + "  url: " + url)
                    success = True
                    break
            except:
                pass
        if not success:
            print("failed eventually ; url : " + url)


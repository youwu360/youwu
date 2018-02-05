import os
import json
import urllib.request
import shutil
import hashlib
import threading
from pyseaweed import WeedFS



class ImageDownloadHelper(object):

    add = 'add'
    minus = 'minus'

    starCover = 'starCover'
    albumCover = 'albumCover'
    albumToStar = 'albumToStar'
    albumImageList = 'albumImageList'

    daolianSize = 4039
    daolianSizeList = [4039, 8192, 6404]
    sizeLowerBound = 1000
    sizeUppderBound = 15000000

    basePath = os.path.dirname(os.path.realpath(__file__))

    starCoverPatterns = ["https://img.onvshen.com:85/girl/__sub__/",
                         "https://t1.onvshen.com:85/girl/__sub__/"]

    albumCoverPatterns = ["https://img.onvshen.com:85/gallery/__sub__/cover/",
                     "https://t1.onvshen.com:85/gallery/__sub__/cover/"]

    imagePatterns = ['https://img.onvshen.com:85/gallery/__sub__/',
                     'https://img.onvshen.com:85/gallery/__sub__/s/',
                     'https://t1.onvshen.com:85/gallery/__sub__/s/',
                     'https://t1.onvshen.com:85/gallery/__sub__/']

    def download_star_cover(self, localAlbumDir, cover_url, starId):
        albumId = None
        self.down_load_image_async(localAlbumDir, cover_url, starId, albumId, self.starCoverPatterns)

    def download_album_cover(self, localAlbumDir, cover_url, starId, albumId):
        self.down_load_image_async(localAlbumDir, cover_url, starId, albumId, self.albumCoverPatterns)

    def download_album_image(self, localAlbumDir, image_url, starId, albumId):
        self.down_load_image_async(localAlbumDir, image_url, starId, albumId, self.imagePatterns)

    def get_hash_code(self, starId, albumId):
        if starId is None:
            starId = ""
        if albumId is None:
            albumId = ""
        res = hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2]
        return str(res)

    def down_load_image_async(self, localAlbumDir, image_url, starId, albumId, imagePatterns):
        t = threading.Thread(target=self.down_load_image,
            args=(localAlbumDir, image_url, starId, albumId, imagePatterns,))
        t.setDaemon(True)
        t.start()

    def down_load_image(self, localAlbumDir, url, starId, albumId, imagePatterns):
        if imagePatterns[0] == self.albumCoverPatterns[0]:
            img_name = 'cover.jpg'
        else:
            img_name = url.split('/')[-1]
        img_path = os.path.join(os.path.join(localAlbumDir, img_name))
        if os.path.exists(img_path):
            if not self.invalid_file_and_contine(img_path):
                print("already exists url : " + url)
                return
            else:
                print('invalid file; retry image : ' + url)

        try:
            urllib.request.urlretrieve(url, img_path)
        except Exception as e:
            print(e)

        if not self.invalid_file_and_contine(img_path):
            print("success url : " + url)
            return

        if albumId is None:
            self.download_star_cover_by_pattern(starId, url, img_path, imagePatterns)
        else:
            self.download_album_by_pattern(starId, albumId, url, img_path, imagePatterns)

    def download_album_by_pattern(self, starId, albumId, url, img_path, imagePatterns):
        success = False
        arr = url.split('/')
        for image_pattern in imagePatterns:
            try:
                new_url = image_pattern.replace('__sub__',
                    str(starId) + "/" + str(albumId)) + arr[-1]
                urllib.request.urlretrieve(new_url, img_path)
                if not self.invalid_file_and_contine(img_path):
                    print("success url by pattern : " + image_pattern + "  url: " + url)
                    success = True
                    break
            except:
                pass
        if not success:
            print("failed eventually ; url : " + url)

    def download_star_cover_by_pattern(self, starId, url, img_path, imagePatterns):
        success = False
        arr = url.split('/')
        for image_pattern in imagePatterns:
            try:
                new_url = image_pattern.replace('__sub__', str(starId)) + arr[-1]
                urllib.request.urlretrieve(new_url, img_path)
                if not self.invalid_file_and_contine(img_path):
                    print("success url by pattern : " + image_pattern + "  url: " + url)
                    success = True
                    break
            except:
                pass
        if not success:
            print("failed eventually ; url : " + url)

    def load_file_to_json(self, filePath):
        if os.path.exists(filePath):
            try:
                with open(filePath) as fp:
                    return json.load(fp)
            except:
                pass
        return self.default_dict()

    #starCover, albumCover, albumToStar, albumImageList
    def join_result(self, json1, json2, action):
        res = {}
        res[self.starCover] = self.join_dict(json1['starCover'], json2['starCover'], action)
        res[self.albumCover] = self.join_dict(json1['albumCover'], json2['albumCover'], action)
        res[self.albumToStar] = self.join_dict(json1['albumToStar'], json2['albumToStar'], self.add)
        res[self.albumImageList] = self.join_dict(json1['albumImageList'], json2['albumImageList'], action)
        return res

    def join_dict(self, d1, d2, action):
        if d1 is None:
            res = {}
        else:
            res = d1

        if d2 is not None:
            for k in d2:
                val = d2[k]
                if type(val) is dict:
                    res[k] = self.join_dict(d1[k] if k in d1 else None,
                                            d2[k] if k in d2 else None
                                            , action)
                else:
                    if action == 'add':
                        if k not in d1:
                            res[k] = d2[k]
                    elif action == 'minus':
                        if k in res:
                            res.pop(k)

        return res

    def invalid_file_and_contine(self, imgFullPath):
        print(imgFullPath)
        if not os.path.exists(imgFullPath):
            print("img path not exists : " + imgFullPath)
            return True

        fileSize = os.path.getsize(imgFullPath)
        if fileSize in self.daolianSizeList:
            os.remove(imgFullPath)
            print("daolian size : " + imgFullPath)
            return True
        elif fileSize == 0:
            os.remove(imgFullPath)
            print("null image, continue " + imgFullPath)
            return True
        elif fileSize >= self.sizeUppderBound:
            os.remove(imgFullPath)
            print("too large file, removed ! fileSize:" + str(fileSize) + " fileName:" + imgFullPath)
            return True
        elif fileSize <= self.sizeLowerBound:
            os.remove(imgFullPath)
            print("too small file, removed ! fileSize:" + str(fileSize) + " fileName:" + imgFullPath)
            return True

    def default_dict(self):
        res = {}
        starCover = self.starCover
        albumCover = self.albumCover
        albumToStar = self.albumToStar
        albumImageList = self.albumImageList
        res[starCover] = {}
        res[albumCover] = {}
        res[albumToStar] = {}
        res[albumImageList] = {}
        return res

    def get_local_product_data_url_json(self):

        basePath = os.path.dirname(os.path.realpath(__file__))
        dataPath = os.path.join(basePath, "data")

        print(dataPath)
        for sub in os.listdir(dataPath):
            subPath = os.path.join(dataPath, sub)
            if os.path.isfile(subPath):
                continue

            print(subPath)
            for album in os.listdir(subPath):
                albumPath = os.path.join(subPath, album)
                if os.path.isfile(albumPath):
                    continue

                albumInJson = album + ".json"
                albumInJsonPath = os.path.join(subPath, albumInJson)

                processedImg = {}
                if os.path.exists(albumInJsonPath):
                    fp = open(albumInJsonPath)
                    processedImg = json.load(fp)

                print(albumPath)
                arr = album.split('.')
                starId = arr[0]
                albumId = arr[1]
                for img in os.listdir(albumPath):

                    imgFullPath = os.path.join(albumPath, img)
                    print(imgFullPath)
                    if self.invalid_file_and_contine(imgFullPath):
                        continue

                    res[albumToStar][albumId] = starId
                    if img == 'cover.jpg':
                        res[albumCover][starId] = True
                        if img in processedImg:
                            res[albumCover][starId] = processedImg[img]
                    else:
                        if albumId not in res[albumImageList]:
                            res[albumImageList][albumId] = {}
                            res[albumImageList][albumId][img] = True

                            if img in processedImg:
                                res[albumImageList][albumId][img] = processedImg[img]
        return res

    def get_local_product_cover_url_json(self):
        res = self.default_dict()
        basePath = os.path.dirname(os.path.realpath(__file__))
        dataPath = os.path.join(basePath, "cover")

        print(dataPath)
        allCoverJsonPath = os.path.join(dataPath, 'allStarCover.json')

        cachedStarCover = {}
        if os.path.exists(allCoverJsonPath):
            fp = open(allCoverJsonPath)
            cachedStarCover = json.load(fp)

        for sub in os.listdir(dataPath):
            subPath = os.path.join(dataPath, sub)
            if os.path.isfile(subPath):
                continue

            print(subPath)
            for starCoverImg in os.listdir(subPath):
                starCoverImgPath = os.path.join(subPath, starCoverImg)

                try:
                    starId = starCoverImg.split('.')[0]
                except Exception as e:
                    print(e)
                    print(starCoverImgPath)

                print(starCoverImgPath)
                if self.invalid_file_and_contine(starCoverImgPath):
                    continue

                res[starCover][starId] = True
                if starId in cachedStarCover:
                    res[starCover][starId] = cachedStarCover[starId]

        return res

    def get_cached_data_in_json(self):
        res1 = self.get_local_product_data_url_json()
        res2 = self.get_local_product_cover_url_json()
        res = self.join_result(res1, res2, ins.add)
        return res


class AlbumCoverLoader(object):
    helper = ImageDownloadHelper()
    res = helper.default_dict()

    def load(self, file):
        if os.path.exists(file):
            with open(file) as fp:
                for line in fp:
                    line = line.strip('/ \n\[\]\"\'')
                    if len(line) > 10:
                        print(line)
                        arr = line.split('/')
                        albumId = None
                        for i in range(len(arr)):
                            if arr[i] == 'cover':
                                albumId = arr[i - 1]
                        if albumId is not None:
                            self.res[self.helper.albumCover][albumId] = line
        return self.res

if __name__ == '__main__':
    ins = AlbumCoverLoader()
    res = ins.load('starAndAlbumId.txt')
    print(res)
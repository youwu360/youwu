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

    def load_file_to_json(self, filePath):
        if os.path.exists(filePath):
            try:
                with open(filePath) as fp:
                    return json.load(fp)
            except:
                return None

    #starCover, albumCover, albumToStar, albumImageList
    def join_result(self, json1, json2, action):
        res = {}
        res['starCover'] = self.join_dict(json1['starCover'], json2['starCover'], action)
        res['albumCover'] = self.join_dict(json1['albumCover'], json2['albumCover'], action)
        # res['albumToStar'] = self.join_dict(json1['albumToStar'], json2['albumToStar'], action)
        res['albumImageList'] = self.join_dict(json1['albumImageList'], json2['albumImageList'], action)
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

    def get_local_product_data_url_json(self):

        res = {}
        starCover = 'starCover'
        albumCover = 'albumCover'
        albumToStar = 'albumToStar'
        albumImageList = 'albumImageList'
        res[starCover] = {}
        res[albumCover] = {}
        res[albumToStar] = {}
        res[albumImageList] = {}

        basePath = os.path.dirname(os.path.realpath(__file__))
        dataPath = os.path.join(basePath, "data")
        daolianSize = 4039

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
                    fileSize = os.path.getsize(imgFullPath)
                    if fileSize == daolianSize:
                        os.remove(imgFullPath)
                        print("daolian size : " + imgFullPath)
                        continue
                    elif fileSize == 0:
                        os.remove(imgFullPath)
                        print("null image, continue " + imgFullPath)
                        continue
                    elif fileSize >= 10000000:
                        os.remove(imgFullPath)
                        print("too large file, removed ! fileSize:" + str(fileSize) + " fileName:" + imgFullPath)
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

        res = {}
        starCover = 'starCover'
        albumCover = 'albumCover'
        albumToStar = 'albumToStar'
        albumImageList = 'albumImageList'
        res[starCover] = {}
        res[albumCover] = {}
        res[albumToStar] = {}
        res[albumImageList] = {}

        basePath = os.path.dirname(os.path.realpath(__file__))
        dataPath = os.path.join(basePath, "cover")
        daolianSize = 4039

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
                fileSize = os.path.getsize(starCoverImgPath)
                if fileSize == daolianSize:
                    os.remove(starCoverImgPath)
                    print("daolian size : " + starCoverImgPath)
                    continue
                elif fileSize == 0:
                    os.remove(starCoverImgPath)
                    print("null image, continue " + starCoverImgPath)
                    continue
                elif fileSize >= 10000000:
                    os.remove(starCoverImgPath)
                    print("too large file, removed ! fileSize:" + str(fileSize) + " fileName:" + starCoverImgPath)
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

if __name__ == '__main__':
    ins = ImageDownloadHelper()
    res1 = ins.get_local_product_data_url_json()
    res2 = ins.get_local_product_cover_url_json()
    res = ins.join_result(res1, res2, ins.add)
    print(res)
    if True:
        exit(0)

    starCover = 'starCover'
    albumCover = 'albumCover'
    albumToStar = 'albumToStar'
    albumImageList = 'albumImageList'

    a = {}
    a[starCover] = {}
    a[starCover][1] = 'starcover1'

    a[albumCover] = {}
    a[albumCover][3] = 'adfefe'
    a[albumToStar] = {}
    a[albumToStar][4] = 'xsxx'

    a[albumImageList] = {}
    a[albumImageList][1] = {}
    a[albumImageList][1][12] = 'afdfad'
    a[albumImageList][1][13] = 'afdfad'

    a[albumImageList][2] = {}
    a[albumImageList][2][1] = 'xxxxxx'

    b = {}
    b[starCover] = {}
    b[starCover][1] = 'starcover1'

    b[albumCover] = {}
    b[albumCover][1] = 'adfe'
    b[albumToStar] = {}
    b[albumToStar][1] = 'xxx'

    b[albumImageList] = {}
    b[albumImageList][1] = {}
    b[albumImageList][1][1] = 'adfad'
    b[albumImageList][1][2] = 'axdfad'

    b[albumImageList][2] = {}
    b[albumImageList][2][1] = 'xxxxxx'

    print(a)
    print(b)
    res = ins.join_result(a, b, 'minus')
    print(res)


import os
import json
from pyseaweed import WeedFS
from scrapy_album_image_to_local_helper import ImageDownloadHelper

class WeedUpLoader:

    basePath = os.path.dirname(os.path.realpath(__file__))
    daolianSize = 4039

    image_download_helper = ImageDownloadHelper()
    allUrlsForProduct = image_download_helper.default_dict()
    allStarCoverDataInJson = 'allStarCover.json'
    allUrlsForProductInJsonFile = 'allUrlsForProduct.json'

    def upload_data(self):
        dataPath = os.path.join(self.basePath, "data")
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
                for img in os.listdir(albumPath):
                    if img in processedImg:
                        continue

                    imgFullPath = os.path.join(albumPath, img)
                    print(imgFullPath)

                    if self.image_download_helper.invalid_file_and_contine(imgFullPath):
                        continue

                    w = WeedFS("localhost", 9333)
                    fid = w.upload_file(imgFullPath)
                    img_url = w.get_file_url(fid)
                    #res = w.delete_file(fid)

                    processedImg[img] = img_url
                print(processedImg)
                with open(albumInJsonPath, 'w') as fp:
                    json.dump(processedImg, fp)

    def upload_cover(self):

        dataPath = os.path.join(self.basePath, "cover")
        allCoverJsonPath = os.path.join(dataPath, self.allStarCoverDataInJson)
        cachedStarCover = {}
        if os.path.exists(allCoverJsonPath):
            with open(allCoverJsonPath) as fp:
                cachedStarCover = json.load(fp)

        print(dataPath)
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
                    continue

                print(starCoverImgPath)
                if self.image_download_helper.invalid_file_and_contine(starCoverImgPath):
                    continue

                w = WeedFS("localhost", 9333)
                fid = w.upload_file(starCoverImgPath)
                img_url = w.get_file_url(fid)

                cachedStarCover[starId] = img_url
        print(cachedStarCover)
        with open(allCoverJsonPath, 'w') as fp:
            json.dump(cachedStarCover, fp)

    def generate_all_url_for_product(self):
        dataPath = os.path.join(self.basePath, "cover")
        allCoverJsonPath = os.path.join(dataPath, self.allStarCoverDataInJson)
        cachedStarCover = {}
        if os.path.exists(allCoverJsonPath):
            with open(allCoverJsonPath) as fp:
                cachedStarCover = json.load(fp)
        for starId in cachedStarCover:
            self.add_star_cover(starId, cachedStarCover[starId])

        dataPath = os.path.join(self.basePath, "data")
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

                arr = album.split('.')
                starId = arr[0]
                albumId = arr[1]
                for img in processedImg:
                    if img == 'cover.jpg':
                        self.add_album_cover(starId, albumId, processedImg[img])
                    else:
                        self.add_album_image(starId, albumId, img, processedImg[img])

        allUrlsForProductInJsonFile = os.path.join(self.basePath, self.allUrlsForProductInJsonFile)
        with open(allUrlsForProductInJsonFile, 'w') as fp:
            json.dump(self.allUrlsForProduct, fp)

    def add_star_cover(self, starId, url):
        starCoverDict = self.allUrlsForProduct[self.image_download_helper.starCover]
        starCoverDict[starId] = url
    def add_album_cover(self, starId, albumId, url):
        albumCoverDict = self.allUrlsForProduct[self.image_download_helper.albumCover]
        albumCoverDict[albumId] = url
        self.add_album_to_star(starId, albumId)

    def add_album_image(self, starId, albumId, img, url):
        albumImageListDict = self.allUrlsForProduct[self.image_download_helper.albumImageList]
        if albumId not in albumImageListDict:
            albumImageListDict[albumId] = {}
        albumImageListDict[albumId][img] = url
        self.add_album_to_star(starId, albumId)

    def add_album_to_star(self, starId, albumId):
        albumToStar = self.allUrlsForProduct[self.image_download_helper.albumToStar]
        albumToStar[albumId] = starId


if __name__ == '__main__':
    uploader = WeedUpLoader()
    # uploader.upload_cover()
    # uploader.upload_data()
    uploader.generate_all_url_for_product()

import os
import json
from pyseaweed import WeedFS


class WeedUpLoader:

    basePath = os.path.dirname(os.path.realpath(__file__))
    daolianSize = 4039


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
                    fileSize = os.path.getsize(imgFullPath)
                    if fileSize == self.daolianSize:
                        print("daolian size : " + imgFullPath)
                        continue
                    elif fileSize == 0:
                        print("null image, continue " + imgFullPath)
                        continue
                    elif fileSize >= 10000000:
                        os.remove(imgFullPath)
                        print("too large file, removed ! fileSize:" + str(fileSize) + " fileName:" + imgFullPath)
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
        allStarCoverDataInJson = 'allStarCover.json'
        allCoverJsonPath = os.path.join(dataPath, allStarCoverDataInJson)
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

                print(starCoverImgPath)
                fileSize = os.path.getsize(starCoverImgPath)
                if fileSize == self.daolianSize:
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

                w = WeedFS("localhost", 9333)
                fid = w.upload_file(starCoverImgPath)
                img_url = w.get_file_url(fid)

                cachedStarCover[starCoverImg] = img_url
        print(cachedStarCover)
        with open(allStarCoverDataInJson, 'w') as fp:
            json.dump(cachedStarCover, fp)


if __name__ == '__main__':
    uploader = WeedUpLoader()
    uploader.upload_cover()
    uploader.upload_cover()

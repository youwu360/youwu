import os
import json
from pyseaweed import WeedFS


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
        for img in os.listdir(albumPath):
            if img in processedImg:
                continue

            imgFullPath = os.path.join(albumPath, img)
            print(imgFullPath)
            fileSize = os.path.getsize(imgFullPath)
            if fileSize == daolianSize:
                print("daolian size : " + imgFullPath)
                continue
            elif fileSize == 0:
                print("null image, continue " + imgFullPath)
                continue
            elif fileSize >= 2000000:
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




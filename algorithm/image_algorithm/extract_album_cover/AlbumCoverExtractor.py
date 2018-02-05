import numpy as np
import cv2
import os
import hashlib


class AlbumCoverExtractor:

    basePath = os.path.dirname(os.path.realpath(__file__))

    cascadePath = os.path.abspath(os.path.join(basePath,
                  "../haarcascades/haarcascade_frontalface_default.xml"))
    starAndAlbumIdFile = os.path.abspath(os.path.join(basePath,
                  "starAndAlbumId.txt"))

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(self.cascadePath)

    def get_hash_code(self, starId, albumId):
        if starId is None:
            starId = ""
        if albumId is None:
            albumId = ""
        res = hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2]
        return str(res)

    def extractOneImage(self, imagePath):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=15,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        shape = image.shape
        ratio = 1.0 * shape[0] / shape[1]
        if faces is not None and len(faces) != 0:
            for (x, y, w, h) in faces:
                if w * h * 100 < shape[0] * shape[1]:
                    continue

                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                midX = x + w / 2
                midY = y + h / 2

                cropedImage = image
                if ratio > 1.55:
                    yUp = int(midY - 0.25 * 1.5 * shape[1])
                    yDown = int(midY + 0.75 * 1.5 * shape[1])

                    if yUp < 0:
                        yUp = 0
                        yDown -= yUp
                    elif yDown > shape[0]:
                        yDown = shape[0]
                        yUp -= yDown - shape[0]

                    cropedImage = image[yUp:yDown,:]
                elif ratio < 1.46:
                    xLeft = int(midX - shape[0] / 3.0)
                    xRight = int(midX + shape[0] / 3.0)

                    if xLeft < 0:
                        xLeft = 0
                        xRight -= xLeft
                    elif xRight > shape[1]:
                        xRight = shape[1]
                        xLeft += shape[1] - xRight
                    cropedImage = image[:, xLeft:xRight]
                cropedImage =cv2.resize(cropedImage, (333, 500))
                # cv2.imshow("croped image : " + imagePath, cropedImage)
                path = os.path.join(os.path.dirname(imagePath), "cover.jpg")
                print(path)
                cv2.imwrite(path, cropedImage)
                print("generate cover by face ! ")
                return True
        else:
            print("Faces not found : " + imagePath)
            return False

    def cropOneImage(self, imagePath):
        image = cv2.imread(imagePath)
        shape = image.shape

        xlen = min(shape[0], shape[1] * 1.5)
        ylen = min(shape[1], shape[0] * 1.5)

        cropedImage = image[0:ylen, 0:xlen]
        cropedImage = cv2.resize(cropedImage, (333, 500))

        cover_path = os.path.join(os.path.dirname(imagePath), "cover.jpg")
        print(cover_path)
        cv2.imwrite(cover_path, cropedImage)


    def extractOneAlbum(self, starId, albumId):
        albumImageFileDir = os.path.abspath(os.path.join(self.basePath,
                        "../../../spider/spider_nvshens/scrapy_album_image_to_local/data/"
                        + self.get_hash_code(starId, albumId) + "/"
                        + str(starId) + "." + str(albumId)))
        self.extractOneFolder(albumImageFileDir)

    def extractOneFolder(self, folderPath):
        cover_path = os.path.join(folderPath, 'cover.jpg')
        if os.path.exists(cover_path):
            return

        imageList = os.listdir(folderPath)

        success = False
        for image in imageList:
            if self.extractOneImage(os.path.join(folderPath, image)):
                success = True
                break

        if not success:
            for image in imageList:
                self.cropOneImage(os.path.join(folderPath, image))
                break

    def runWithStarIdAndAlbumId(self):
        with open(self.starAndAlbumIdFile, 'r') as fp:
            lines = fp.readlines()
            print(lines)
            for line in lines:
                if line is None:
                    continue
                line = line.strip()
                print(line)

                if line == '' or line.startswith('#'):
                    continue

                arr = line.split('/')
                self.extractOneAlbum(starId=arr[0], albumId=arr[1])


if __name__ == '__main__':
    ins = AlbumCoverExtractor()
    ins.runWithStarIdAndAlbumId()

import numpy as np
import cv2
import os


class AlbumCoverExtractor:

    basePath = os.path.dirname(os.path.realpath(__file__))

    cascadePath = os.path.abspath(os.path.join(basePath,
                  "../haarcascades/haarcascade_frontalface_default.xml"))
    starAndAlbumIdFile = os.path.abspath(os.path.join(basePath,
                  "starAndAlbumId.txt"))

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(self.cascadePath)

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
        print(shape)
        cv2.imshow("Finding : " + imagePath, image)
        cv2.waitKey(0)
        if faces is not None and len(faces) != 0:
            for (x, y, w, h) in faces:
                if w * h * 100 < shape[0] * shape[1]:
                    continue

                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
                cv2.imshow("croped image : " + imagePath, cropedImage)
                cv2.waitKey(0)

            cv2.imshow("Faces found : " + imagePath, image)
            cv2.waitKey(0)
            return True
        else:
            cv2.imshow("Faces not found : " + imagePath, image)
            cv2.waitKey(0)
            return False

    def extractOneAlbum(self, starId, albumId):
        albumImageFileDir = os.path.abspath(os.path.join(self.basePath,
                        "test_data/" + str(starId) + "." + str(albumId)))
        self.extractOneFolder(albumImageFileDir)

    def extractOneFolder(self, folderPath):
        imageList = os.listdir(folderPath)
        for image in imageList:
            if self.extractOneImage(os.path.join(folderPath, image)):
                print(111)
                # break

    def runWithStarIdAndAlbumId(self):
        with open(self.starAndAlbumIdFile, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                if line is None:
                    continue
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue

                arr = line.split('/')
                self.extractOneAlbum(starId=arr[0], albumId=arr[1])


if __name__ == '__main__':
    ins = AlbumCoverExtractor()
    ins.extractOneFolder('test_data/other_images')

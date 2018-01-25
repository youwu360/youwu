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
            scaleFactor=1.3,
            minNeighbors=20,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if faces is not None and len(faces) != 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
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

        imageList = os.listdir(albumImageFileDir)
        for image in imageList:
            if self.extractOneImage(os.path.join(albumImageFileDir, image)):
                break

    def run(self):
        with open(self.starAndAlbumIdFile, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                if line is None:
                    continue
                line = line.strip()
                if line == '':
                    continue

                arr = line.split('/')
                self.extractOneAlbum(starId=arr[0], albumId=arr[1])


if __name__ == '__main__':
    ins = AlbumCoverExtractor()
    ins.run()

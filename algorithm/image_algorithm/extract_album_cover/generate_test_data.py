import os

basePath = os.path.dirname(os.path.realpath(__file__))
albumIdFile = os.path.join(basePath, "starAndAlbumId.txt")
albumImageListFIlePath = "../../../youwu-resource/data/url_info/"

with open(albumIdFile, 'r') as fp:
    while True:
        line = fp.readline()
        if line is None or line == '':
            break
        line = line.strip()
        arr = line.split('|')
        starId = arr[0]
        albumId = arr[1]
        fileName = str(starId) + "." + str(albumId)
        albumImageListFIle = os.path.join(basePath, albumImageListFIlePath + fileName)

        data





import hashlib

def get_hash_code(starId, albumId):
    res = hashlib.md5((str(starId) + "-" + str(albumId)).encode('utf-8')).hexdigest()[0:2]
    return str(res)
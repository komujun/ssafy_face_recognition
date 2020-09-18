import urllib.request
import os

def getDownload(data):
    cnt = 0
    path_dir = "./picture_utility/picture_before"
    for (path, dir, files) in os.walk(path_dir):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.jpg' or ext == '.png':
                album_id = path.split("/")[3]
                # print(path)
                # print(album_id)
                # print(filename)
                
                data.setAlbumId(album_id)
                data.setPictureId(filename)
                data.setStatus("processing")
                data.setPictureUrl(path + "/" + filename)
                data.setPictureCut("-")
                data.setBox("-")
                data.setEncoding("-")
                cnt += 1

    return cnt
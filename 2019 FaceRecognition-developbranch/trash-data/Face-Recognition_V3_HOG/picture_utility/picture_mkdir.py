import urllib.request
import os

def faceMkdir(path, dirname, album_id):
    if not os.path.isdir(path + dirname):    # 디렉토리 유무 확인
        os.mkdir(path + dirname)             # 없으면 생성하라

    url = path + dirname + "/" + album_id
    if not os.path.isdir(url):               # 디렉토리 유무 확인
        os.mkdir(url)                        # 없으면 생성하라
    
    return 1
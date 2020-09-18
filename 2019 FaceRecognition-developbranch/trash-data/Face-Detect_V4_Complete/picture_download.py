import urllib.request
import os

def getDownload(album_id, picture_id, status, picture_url):
    dirname = "img_before"                         # 체크하고자 하는 디렉토리명
    if not os.path.isdir("./" + dirname + "/"):    # 디렉토리 유무 확인
        os.mkdir("./" + dirname + "/")             # 없으면 생성하라

    dirname += "/" + album_id
    if not os.path.isdir("./" + dirname + "/"):    # 디렉토리 유무 확인
        os.mkdir("./" + dirname + "/")             # 없으면 생성하라

    dirname += "/" + picture_id
    if not os.path.isdir("./" + dirname + "/"):    # 디렉토리 유무 확인
        os.mkdir("./" + dirname + "/")             # 없으면 생성하라

    dirname += "/" + picture_id + ".jpg"
    # print(dirname)

    if os.path.isfile("./" + dirname):
        # print("파일이 이미 있습니다")
        return -1

    urllib.request.urlretrieve(picture_url, dirname)
    try:
        urllib.request.urlretrieve(picture_url, dirname)
        # print("다운로드 완료!")
        return 1
    except:
        # print("다운로드 오류!")
        return -2
    
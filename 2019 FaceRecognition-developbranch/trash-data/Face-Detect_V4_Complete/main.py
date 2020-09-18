import json
import requests
from picture_class import picture_data
from picture_download import getDownload
from picture_search import faceSearch
from picture_detect import faceDetect

# https://docs.google.com/document/d/1lwofKqyqlq--8LuiqjpFgP4R-7mPNt0JT5QwAcu_MRA/edit
# FaceRecognition <-> Server

# https://kidsharu.github.io/KidsHaru-APIDoc/
# 자세한 API 문서

url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing"

# data get
try:
    # URL에서 정보 얻기
    response = requests.get(url)

    # 데이터 추가
    data = picture_data()
    data.append_data(response)
except:
    print("URL 주소 인식 실패")

# picture download
try:
    for i in range(0, data.getLen()):
        album_id = str(data.getAlbumId(i)).strip()
        picture_id = str(data.getPictureId(i)).strip()
        status = data.getStatus(i)
        picture_url = str(data.getPictureUrl(i)).strip()
        # print(album_id, picture_id, status, picture_url)
        download = getDownload(album_id, picture_id, status, picture_url)
except:
    print("사진을 저장하는데 실패하였습니다.")

# picture detecting
try:
    for i in range(0, 5):
        print(i)
        album_id = str(data.getAlbumId(i)).strip()
        picture_id = str(data.getPictureId(i)).strip()
        status = data.getStatus(i)
        picture_url = str(data.getPictureUrl(i)).strip()

        print(album_id, picture_id, status, picture_url)
        img_before, img_after = faceSearch(album_id, picture_id, status, picture_url)

        if(img_before != -1 and img_after != -1):
             checking = faceDetect(album_id, picture_id, status, picture_url, img_before, img_after)

        '''
        checking = 1
        if(checking == 1):
            put_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/" + str(album_id) + "/pictures/" + str(picture_id)
        
        json_data = {
             "status" : 'processing'
        }
        json_string = json.dumps(json_data).encode("utf-8")
        response = requests.put(put_url, data=json_string)

        json_data = {
           "status" : "checking"
        } 
        json_string = json.dumps(json_data).encode("utf-8")
        response = requests.put(put_url, data=json_string)
        '''
except:
    print("사진을 처리하는데 실패하였습니다.")

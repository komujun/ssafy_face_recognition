import json
import requests
import pickle
from picture_utility import picture_class as pc
from picture_utility import picture_download as pdl
from picture_utility import picture_detect as pdt
from picture_utility import picture_pickle as pp
from clustering_utility import face_clustering as fc

# https://docs.google.com/document/d/1lwofKqyqlq--8LuiqjpFgP4R-7mPNt0JT5QwAcu_MRA/edit
# FaceRecognition <-> Server

# https://kidsharu.github.io/KidsHaru-APIDoc/
# 자세한 API 문서

url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing"

# URL에서 정보 얻기
data = pc.picture_data()
response = requests.get(url)

cnt = 0
# data get
try:
    # URL에서 정보 얻기
    data = pc.picture_data()
    response = requests.get(url)

    for i in response.json():
        data.setAlbumId(i['album_id'])
        data.setStatus(i['status'])
        data.setPictureIdData(i['picture_id'])
        data.setPictureUrl(i['picture_url'])

        data.setPictureId("-")
        data.setPictureCut("-")
        data.setBox("-")
        data.setEncoding("-")
        cnt = cnt + 1

except:
    print("URL 주소 인식 실패")


# picture download
try:
    for i in range(0, data.getLen()):
        data.ResetPictureId(i, data.getPictureUrl(i).split('/')[5])

        album_id = str(data.getAlbumId(i)).strip()
        picture_id = str(data.getPictureId(i)).strip()
        status = data.getStatus(i)
        picture_url = str(data.getPictureUrl(i)).strip()
        
        # print(album_id, picture_id, status, picture_url)
        download = pdl.getDownload(album_id, picture_id, status, picture_url)
except:
    print("사진을 저장하는데 실패하였습니다.")


# picture detecting, encoding
for i in range(cnt):
    album_id = str(data.getAlbumId(i)).strip()
    picture_id = str(data.getPictureId(i)).strip()
    status = data.getStatus(i)
    picture_url = str(data.getPictureUrl(i)).strip()

    box, encoding, cut_url = pdt.faceDetect(album_id, picture_id, status, picture_url)
    # print(box, encoding)

    if box == -1 and encoding == -1 and cut_url == -1:
        # print('이미 처리된 파일입니다.')
        box = -1
        encoding = -1
        cut_url = -1
    else:
        data.ResetBox(i, box)
        data.ResetEncoding(i, encoding)
        data.ResetPictureCut(i, cut_url)
        # print(box)

# picture pickle
data2 = pc.picture_data()
pp.ReadPickle(data2)

for i in range(cnt):
    if(data.getBox(i) != '-' and data.getEncoding(i) != '-'):
        pp.WriteAppendFile(data, data2, i)

ecnt, check, img= fc.clustering(data2)

count = ecnt
# picture
for i in range(cnt):
    album_id = str(data2.getAlbumId(i)).strip()
    picture_id_data = str(data2.getPictureIdData(i)).strip()
    status = data2.getStatus(i)
    picture_url = str(data2.getPictureUrl(i)).strip()
    
    # print(i, img)
    if status == "processing":
        post_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/" + str(picture_id_data) + "/faces"
        print(post_url)

        # top:bottom, left:right
        child_id = []
        rect_x = []
        rect_y = []
        rect_width = []
        rect_height = []
        # top, right, bottom, left
        for j in range(len(data2.getBox(i))):
                if check[count] == "-":
                    check[count] = -1

                json_data = {
                        'child_id' : int(check[count]),
                        'rect_x' : data2.getBox(i)[j][3],
                        'rect_y' : data2.getBox(i)[j][0],
                        'rect_width' : data2.getBox(i)[j][1] - data2.getBox(i)[j][3],
                        'rect_height' : data2.getBox(i)[j][2] - data2.getBox(i)[j][0]
                }
                print(json_data)
                print(img[count])
                json_string = json.dumps(json_data).encode("utf-8")
                response = requests.post(post_url, data=json_string)
                count += 1

    data2.ResetStatus(i, "complete")


pp.WritePickle(data2)
print(data2.getLen())


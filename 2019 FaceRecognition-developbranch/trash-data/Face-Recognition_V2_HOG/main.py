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

# picture path 확인, 나누기
data = pc.picture_data()
cnt = pdl.getDownload(data)

# picture detecting, encoding
for i in range(cnt):
    album_id = data.getAlbumId(i).strip()
    picture_id = data.getPictureId(i).strip()
    status = data.getStatus(i).strip()
    picture_url = data.getPictureUrl(i).strip()

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
        print(cut_url)

# picture pickle
data2 = pc.picture_data()
pp.ReadPickle(data2)

for i in range(cnt):
    if(data.getBox(i) != '-' and data.getEncoding(i) != '-'):
        pp.WriteAppendFile(data, data2, i)

pp.WritePickle(data2)
# print(data2.getLen())

fc.clustering(data2)


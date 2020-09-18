from sklearn.cluster import DBSCAN
import pickle
import numpy as np
import os
import signal
import sys
import cv2
from PIL import Image
import model_custom
from picture_utility import picture_mkdir as pm

def faceDetect(album_id, picture_id, status, picture_url):
    # (top, right, bottom, left)
    global top, right, bottom, left

    dirname = "picture_after"
    if os.path.isfile("./picture_utility/" + dirname + "/" + album_id + "/" + picture_id):    # 디렉토리 유무 확인
        # print("./picture_utility/" + dirname + "/" + album_id + "/" + picture_id)
        return -1, -1, -1

    # 이미지 인식
    dirname = "picture_before"
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread("./picture_utility/" + dirname + "/" + album_id + "/" + picture_id)

    # HOG 모델로 face_detecting 완료
    box = model_custom.face_locations(img, model="hog")

    temp = img.copy()
    # Rectangle 사각형
    for top, right, bottom, left in box:
        cv2.rectangle(temp, (left, top), (right, bottom), (0, 255, 0), 2)

    # Encoding
    encoding = model_custom.face_encodings(img, box)

    # write dir
    dirname = "picture_after"
    pm.faceMkdir("./picture_utility/", dirname, album_id)
    cv2.imwrite("./picture_utility/" + dirname + "/" + album_id + "/" + picture_id, temp)

    dirname1 = "picture_cut"
    if len(box) >= 1:
        pm.faceMkdir("./picture_utility/", dirname1, album_id)
    cnt = 1
    cut_url = []
    for top, right, bottom, left in box:
        crop_img = img[top:bottom, left:right]
        re_img_id = picture_id.split('.')
        
        cut_url.append("./picture_utility/" + dirname1 + "/" + album_id + "/" + re_img_id[0] + "_" + str(cnt) + "." + re_img_id[1])
        cv2.imwrite(cut_url[cnt-1], crop_img)
        cnt += 1

    # message
    # print('Face Detecting 완료!')
    # print(box)

    return box, encoding, cut_url
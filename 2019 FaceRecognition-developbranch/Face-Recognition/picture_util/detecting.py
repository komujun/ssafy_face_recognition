import cv2
import numpy as np
import model_custom

def faceDetect(data):
    global top, right, bottom, left

    # 이미지 인식
    dirname = data['picture_url'] + "/" + data['picture_name']
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(dirname)

    # 800으로 image 사이즈 조정
    height, width, channel = img.shape
    if height >= width:
        x = 800 / height
    else:
        x = 800 / width
    img_t = cv2.resize(img, dsize=(0, 0), fx= x, fy= x, interpolation=cv2.INTER_LINEAR)

    # 노말라이징
    dst = np.zeros(shape=(5,2))
    norm_img = cv2.normalize(img_t, dst, 0, 255, cv2.NORM_MINMAX)

    # CNN 모델로 face_detecting 완료
    box = model_custom.face_locations(norm_img, model="cnn")
    # print(box)

    box_list = []
    for top, right, bottom, left in box:
        box_list.append( ( int(top/x), int(right/x), int(bottom/x), int(left/x) ) )

    # print(box_list)
    # Encoding
    encoding = model_custom.face_encodings(norm_img, box)
    # print(encoding)

    # temp = img.copy()
    # Rectangle 사각형
    # for top, right, bottom, left in box_list:
        # cv2.rectangle(temp, (left, top), (right, bottom), (0, 255, 0), 2)
        # print(top, right, bottom, left)

    # cv2.imshow("test", temp)
    # cv2.waitKey(0)
    
    return box_list, encoding


def WebfaceDetect(dirname, data):
    global top, right, bottom, left

    # 이미지 인식
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(dirname)

    # 800으로 image 사이즈 조정
    height, width, channel = img.shape
    if height >= width:
        x = 800 / height
    else:
        x = 800 / width
    img_t = cv2.resize(img, dsize=(0, 0), fx= x, fy= x, interpolation=cv2.INTER_LINEAR)

    # 노말라이징
    dst = np.zeros(shape=(5,2))
    norm_img = cv2.normalize(img_t, dst, 0, 255, cv2.NORM_MINMAX)

    # CNN 모델로 face_detecting 완료
    box = model_custom.face_locations(norm_img, model="cnn")

    box_list = []
    for top, right, bottom, left in box:
        box_list.append( ( int(top/x), int(right/x), int(bottom/x), int(left/x) ) )
    # print(box_list)

    # print(box_list)
    # Encoding
    encoding = model_custom.face_encodings(norm_img, box)
    # print(encoding)

    # temp = img.copy()
    # Rectangle 사각형
    # for top, right, bottom, left in box_list:
        # cv2.rectangle(temp, (left, top), (right, bottom), (0, 255, 0), 2)
        # print(top, right, bottom, left)

    # cv2.imshow("test", temp)
    # cv2.waitKey(0)
    
    return box_list, encoding

    
import numpy as np
import cv2
import sys
import requests
import json
import urllib.request
import os

def faceDetect(album_id, picture_id, status, picture_url, img_before, img_after):
    global x, y, w, h

    font = cv2.FONT_HERSHEY_SIMPLEX
    cascPath = "haarcascade_frontface.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    
    # 계산 반복 횟수 (한번만 처리하려면 아래를 1로 하거나 for문을 제거하세요)
    iteration_count = 1
    for cnt in range(0, iteration_count):
        # Read the image
        image = cv2.imread("./" + img_before)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,     # 이미지에서 얼굴 크기가 서로 다른 것을 보상해주는 값
            minNeighbors=5,    # 얼굴 사이의 최소 간격(픽셀)입니다
            minSize=(10, 10),   # 얼굴의 최소 크기입니다
        )

        post_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/" + str(album_id) + "/pictures/" + str(picture_id) + "/children"
        print(post_url)

        num = 1
        # 검출된 얼굴 주변에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(x, y, w, h)
            
            delete_url = post_url + "/" + str(num)
            # print(delete_url)
            json_data = {
                "album_id" : int(album_id),
                "picture_id" : int(picture_id),
                "child_id": int(num), 
                "rect_x": int(x), 
                "rect_y": int(y), 
                "rect_width": int(w), 
                "rect_height": int(h)
                }
            
            json_string = json.dumps(json_data).encode("utf-8")
 
            response = requests.delete(delete_url)
            response = requests.post(post_url, data=json_string)
            num += 1

        cv2.imwrite("./" + img_after, image)
        print('저장 완료!')
        
    print('처리 성공!')
    return 1
    
    
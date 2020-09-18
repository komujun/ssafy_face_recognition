import numpy as np
import cv2
import sys

font = cv2.FONT_HERSHEY_SIMPLEX
def faceDetect():
    cascPath = "haarcascade_frontface.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    from datetime import datetime
    start_time = datetime.now()
    
    # 계산 반복 횟수 (한번만 처리하려면 아래를 1로 하거나 for문을 제거하세요)
    iteration_count = 100
    for cnt in range(0, iteration_count):
        # Read the image
        # image = cv2.imread('https://s3.ap-northeast-2.amazonaws.com/kidsharu-album/9/0dec6019b3efaff846ff5f3d8fb7a174.jpg')
        image = cv2.imread('001.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,     # 이미지에서 얼굴 크기가 서로 다른 것을 보상해주는 값
            minNeighbors=5,    # 얼굴 사이의 최소 간격(픽셀)입니다
            minSize=(20, 20),   # 얼굴의 최소 크기입니다
        )

        # 검출된 얼굴 주변에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        average_time = elapsed_time / iteration_count
        
        print("Elapsed Time: %s sec" % elapsed_time)
        print("Average Time: %s sec" % average_time)

        # 얼굴을 검출한 이미지를 화면에 띄웁니다
        cv2.imshow("Face Detected", image)
        
        # 아무 키나 누르면 빠져나옵니다
        cv2.waitKey(0)

# image = cv2.imread("https://s3.ap-northeast-2.amazonaws.com/kidsharu-album/9/0dec6019b3efaff846ff5f3d8fb7a174.jpg")

# print(image)
# cv2.imshow("Face Detected", image)
        
# 아무 키나 누르면 빠져나옵니다
# cv2.waitKey(0)
faceDetect()
# 출처: http://kinocoder.tistory.com/34 [키노코더 이야기]
# https://www.popit.kr/openface-exo-member-face-recognition/
# http://jayharvey.tistory.com/10
# https://www.popit.kr/torch%EC%99%80-opencv%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%8B%A4%EC%8B%9C%EA%B0%84-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%B6%84%EB%A5%98-%EB%8D%B0%EB%AA%A8/
# https://github.com/jaeho-kang/deep-learning/tree/master/library/openface
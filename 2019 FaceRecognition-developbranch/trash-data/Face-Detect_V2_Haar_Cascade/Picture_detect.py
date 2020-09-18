import numpy as np
import cv2
import sys

#############################################################
def faceDetect(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cascPath = "haarcascade_frontface.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    from datetime import datetime
    start_time = datetime.now()
    
    # 계산 반복 횟수 (한번만 처리하려면 아래를 1로 하거나 for문을 제거하세요)
    iteration_count = 1
    for cnt in range(0, iteration_count):
        # Read the image
        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,     # 이미지에서 얼굴 크기가 서로 다른 것을 보상해주는 값
            minNeighbors=3,    # 얼굴 사이의 최소 간격(픽셀)입니다
            minSize=(10, 10),   # 얼굴의 최소 크기입니다
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
#############################################################
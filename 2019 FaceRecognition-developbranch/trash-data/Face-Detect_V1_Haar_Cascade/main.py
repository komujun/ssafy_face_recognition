import requests
import numpy as np
import cv2
import sys

#############################################################
class Picture_ID:
    def __init__(self):
        self.album_id = []
        self.picture_id = []
        self.status = []
        self.picture_url = []
    
    def append_id(self, response):
        for i in response.json():
            self.album_id.append(i['album_id'])
            self.picture_id.append(i['picture_id'])
            self.status.append(i['status'])
            self.picture_url.append(i['picture_url'])

    def print_id(self):
        for i in range(len(self.picture_url) - 1):
            print(self.picture_url[i])

    def destroy_id(self):
        self.album_id = []
        self.picture_id = []
        self.status = []
        self.picture_url = []

    def getAlbumId(self, x):
        return self.album_id[x]

    def getPictureId(self, x):
        return self.picture_id[x]

    def getStatus(self, x):
        return self.status[x]

    def getPictureUrl(self, x):
        return self.picture_url[x]

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
            minSize=(5, 5),   # 얼굴의 최소 크기입니다
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


url = 'https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing'
response = requests.get(url)

try:
    data = Picture_ID()
    data.append_id(response)
except:
    print("사이트를 읽는데 실패하였습니다.")

try:
    faceDetect(str(data.getPictureUrl(0)).strip())
except:
    print("이미지를 처리하는데 실패했습니다.")

# print( data.print_id() )
print( data.getPictureUrl(1) )

faceDetect( data.getPictureUrl(1) )
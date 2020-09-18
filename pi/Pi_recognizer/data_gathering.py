import cv2
import os
import sys
import zipfile
import shutil
from flask_opencv_streamer.streamer import Streamer
streamer=Streamer(8080,False)

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_id = sys.argv[1]
font = cv2.FONT_HERSHEY_SIMPLEX

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0

while(True):
    ret, img = cam.read()
    img = cv2.flip(img, 0) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.putText(img, str(count)+" of "+ str(30), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        cv2.imshow('image', img)
        print(count)
    streamer.update_frame(img)
    if not streamer.is_streaming:
        streamer.start_streaming()
        
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         img=cv2.imread("done.jpg",1)
         cv2.imshow('image', img)
         streamer.update_frame(img)
         break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
shutil.make_archive('./dataset','zip','./dataset')
#shutil.rmtree('./dataset')
#os.mkdir('./dataset')
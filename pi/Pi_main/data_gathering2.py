import cv2
import os
import sys
import shutil
#import socket
#from flask_opencv_streamer.streamer import Streamer
#streamer=Streamer(8080,False)
face_id=sys.argv[1]
receiveno = 0
minW=150
minH=150

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0) #cam initialize
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
count=0
while(True): #capture start
    ret, img = cam.read()
    img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 5, minSize = (int(minW), int(minH)))

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.putText(img, str(count)+" of "+ str(30), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    cv2.imshow('video',img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 31: # Take 30 face sample and stop video
         img=cv2.imread("done.jpg",1)
         cv2.imshow('image', img)
         break;
# Do a bit of cleanup
print("\n [+]Shutting down Cam")
cam.release()
cv2.destroyAllWindows()

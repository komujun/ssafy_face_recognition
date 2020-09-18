import cv2
import numpy as np
import os
import pymysql
from datetime import datetime,timedelta
from flask_opencv_streamer.streamer import Streamer

connection=pymysql.connect(host='i3a207.p.ssafy.io',user='a207',password='a207',db='mydbtest',charset='utf8',autocommit=True)
cursor=connection.cursor()
print("DB access success")

id_user="SELECT blog_usergroup.id,eng_name,enter_at, out_at FROM blog_usergroup INNER JOIN blog_access ON blog_usergroup.ID=blog_access.user_pk_id ORDER BY enter_at ASC"
plist={}
tester={}
execute_user=cursor.execute(id_user)
for row in cursor:
    plist.update({row[0]:{'name':row[1],'enter_at':row[2],'out_at':row[3]}})
    tester.update({row[0]:0})
print("Successfully gathered datas from DB")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
cam = cv2.VideoCapture(0) # Initialize and start video capture
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 100
minH = 100

streamer=Streamer(8080,False) #for web
nowtime=datetime.now()
nowtime_UTC=nowtime-timedelta(hours=9)
trainer_updatedday=nowtime.day
print("Camera ON")

while True:
    ret, img =cam.read()
    img = cv2.flip(img, 0) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
    )
    nowtime=datetime.now()
    nowtime_UTC=nowtime-timedelta(hours=9)
    if(nowtime.day!=trainer_updatedday): #update trainer file at 24:00
        os.system('python3 trainer.py')
        trainer_updatedday=nowtime.day
        recognizer.read('trainer/trainer.yml')
        print('trainer updated')
        execute_user=cursor.execute(id_user)
        for row in cursor:
            plist.update({row[0]:{'name':row[1],'enter_at':row[2],'out_at':row[3]}})
        print("Successfully gathered datas from DB")
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence < 90): # confidence = 0 is perfect match 
            idno=id
            id = plist[id]["name"]
            confidence = "  {0}%".format(round(100 - confidence))
           # cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            
            if(tester[idno]<10):
                tester[idno]=tester[idno]+1
            elif(tester[idno]>=10):
                if ((plist[idno]["out_at"] is not None) and ((nowtime_UTC-plist[idno]["out_at"]).seconds>=10)):
                    plist[idno].update(enter_at = nowtime_UTC)
                    plist[idno].update(out_at=None)
                    cursor.execute("INSERT blog_access SET user_pk_id= %s, enter_at = %s,recent = %s",(idno,nowtime_UTC,nowtime_UTC))
                    print("Enter: "+id)
                    for key in tester.keys():
                        tester[key]=0
                elif((plist[idno]["out_at"] is None) and (nowtime_UTC-plist[idno]["enter_at"]).seconds>=10):
                    plist[idno].update(out_at = nowtime_UTC)
                    cursor.execute("UPDATE blog_access SET out_at = %s,recent = %s WHERE user_pk_id = %s ORDER BY enter_at DESC LIMIT 1",(nowtime_UTC,nowtime_UTC,idno))
                    print("Out  : "+id)
                    for key in tester.keys():
                        tester[key]=0
                    if(nowtime.hour>=17): #MachineLearning
                        cv2.imwrite("dataset/User." + str(idno) + '.' + str(nowtime.day) + ".jpg", gray[y:y+h,x:x+w])
                        print("New image for "+id+" saved")
        else :
            id = "unknown"
          #  confidence = "  {0}%".format(round(100 - confidence))
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
 #   cv2.imshow('camera',img) 
    streamer.update_frame(img)
    if not streamer.is_streaming:
        streamer.start_streaming()
 #   k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
  #  if k == 27:
  #     break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

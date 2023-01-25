import os
import cv2
import numpy as np
from datetime import datetime
import faceRecognition as fr
import sendemail
import door
import time
# Mail id
mid=['sharonblessyp2001','rnithisree20']

def markAttendance(name,matchIndex):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')

            dtime = dtString.split(":")
            # print(dtime)
            if int(dtime[0]) <= 23 and int(dtime[1]) <= 59:

                msg = "Present"
                f.writelines(f'\n{name},{dtString},{msg}')
                sendemail.send(name,msg,mid[matchIndex]+'@gmail.com',dtime,1)
                print("ACCESS GRANTED")
                # For arduino connection

                door.doorautomate(0)
                time.sleep(6)
                door.doorautomate(1)

            elif (int(dtime[0]) == 8 and int(dtime[1]) <= 59) or (int(dtime[0]) == 8 and int(dtime[1]) >= 31):
                minit = str(int(dtime[1]) - 30)
                stmt = " Minutes Late"
                msg = minit + stmt
                print("ACCESS GRANTED")
                # For arduino connection

                door.doorautomate(0)
                time.sleep(6)
                door.doorautomate(1)

                f.writelines(f'\n{name},{dtString},{msg}')
                sendemail.send(name,msg,mid[matchIndex]+'@gmail.com',dtime,1)

            else:
                msg = "Absent"
                f.writelines(f'\n{name},{dtString},{msg}')

                sendemail.send(name,msg,mid[matchIndex]+'@gmail.com',dtime,0)
                print("ACCESS DENIED")

#captures images via webcam and performs face recognition
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('trainingData.yml')#Load saved training data

name = {0 : "Sharon Blessy",1 :"Nithya"}


cap=cv2.VideoCapture(0)

while True:
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    faces_detected,gray_img=fr.faceDetection(test_img)



    for (x,y,w,h) in faces_detected:
      cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('face detection ',resized_img)
    cv2.waitKey(1)


    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+w, x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
        print("confidence:",confidence)
        print("label:",label)
        fr.draw_rect(test_img,face)
        predicted_name=name[label]
        if confidence <= 35:
           fr.put_text(test_img,predicted_name,x,y)
           markAttendance(predicted_name, label)


    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('face recognition ',resized_img)
    if cv2.waitKey(1) == ord('q'):#wait until 'q' key is pressed
        break


cap.release()
cv2.destroyAllWindows


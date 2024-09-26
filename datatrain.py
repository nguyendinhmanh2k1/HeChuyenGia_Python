import cv2
import numpy as np
import sqlite3
import os


def insertOrUpdate(id, name):
    # conn = sqlite3.connect('C:\\Users\\manhn\\OneDrive\\Desktop\\hcg_python\\data.db')
    conn = sqlite3.connect('D:\\nam 4\\demoo\\hcg_python\\data.db')

    query = "SELECT * FROM people WHERE ID="+ str(id)
    cusror = conn.execute(query)

    isRecordExit = 0

    for row in cusror:
        isRecordExit = 1

    if(isRecordExit == 0):
        query = "INSERT INTO people(ID, Name) VALUES("+str(id)+ ",'"+ str(name)+ "')"
    else :
        query = "UPDATE people SET Name='"+str(name)+"'WHERE ID="+ str(id)
    
    conn.execute(query)
    conn.commit()
    conn.close()

# insertOrUpdate(1,"manhnd")
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_cascade =cv2.CascadeClassifier('haarcascades/hearcascade_fromtalface_alt.xml')

cap = cv2.VideoCapture(0)

#insert to db

id = input("Enter you ID: ")
name = input("Enter you Name: ")
insertOrUpdate(id, name)

sampleNum = 0
while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces :
        cv2.rectangle(frame, (x, y), (x+ w, y+ h) , (0,255,0), 2)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        
        sampleNum +=1

        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNum)+ '.jpg', gray[y: y+ h, x: x+ w])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if sampleNum >99:
        break;

cap.release()
cv2.destroyAllWindows()














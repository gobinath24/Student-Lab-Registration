import cv2  import numpy as np import face_recognition  import os from datetime import datetime  from flask import Flask, render_template,Response  
# from PIL import ImageGrab from random import randint app = Flask(__name__)  path = 'ImagesAttendance' images = []  classNames = []  myList = os.listdir(path) print(myList)  for cl in myList:  
    curImg = cv2.imread(f'{path}/{cl}')     images.append(curImg)     classNames.append(os.path.splitext(cl)[0]) print(classNames)  def findEncodings(images):      encodeList = []     for img in images:          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)         encode = face_recognition.face_encodings(img)[0]         encodeList.append(encode)      return encodeList  def markAttendance(name, mode):      with open('Attendance.csv', 'r+') as f:          myDataList = f.readlines()         nameList = []          for line in myDataList:  
            entry = line.strip().split(',')             
nameList.append(entry[0])       
   now = datetime.now()          dtString = now.strftime('%H:%M:%S')  
        if mode == 'in':              if name not in nameList:  
                newEntry = f'{name},{randint(100,999)},{dtString},{0}\n'                 myDataList.append(newEntry)        
  elif mode == 'out':              for i, line in enumerate(myDataList):  
               entry = line.strip().split(',')                 if entry[0] == name:                      entry[3] = dtString                      myDataList[i] = ','.join(entry) + '\n'                         break  
        f.seek(0)  
        f.writelines(myDataList)  encodeListKnown = findEncodings(images) print('Encoding Complete')  cap = cv2.VideoCapture(0)  
def in_gen():       while True:  
        success, img = cap.read()          #img = captureScreen()          imgS = cv2.resize(img,(0,0),None,0.25,0.25)          imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)          facesCurFrame = face_recognition.face_locations(imgS)         encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)         for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):  
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)             faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)  
            #print(faceDis)             matchIndex = np.argmin(faceDis)             if matches[matchIndex]:  
                name = classNames[matchIndex].upper()  
                #print(name)                  y1,x2,y2,x1 = faceLoc                 y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4                 cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)                 cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)  
                cv2.putText(img,name,(x1+6,y2- 
6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)  
                mod='in'                 
markAttendance(name,mod)          # cv2.imwrite('t.jpg', img)  
   # cv2.imshow('Webcam',img)     # cv2.waitKey(1)          ret, buffer = cv2.imencode('.jpg', img)          frame = buffer.tobytes()          yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        # cap.release() 
def 	out_gen():     
while True:  
        success, img = cap.read()          #img = captureScreen()          imgS = cv2.resize(img,(0,0),None,0.25,0.25)          imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)          facesCurFrame = face_recognition.face_locations(imgS)          encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)         for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):  
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)             faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)  
            #print(faceDis)             matchIndex = np.argmin(faceDis)             if matches[matchIndex]:                  name = classNames[matchIndex].upper()  
                #print(name)                  y1,x2,y2,x1 = faceLoc                  y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4                 cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)                 cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)  
                cv2.putText(img,name,(x1+6,y2- 
6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)  
                mode='out'                 
 markAttendance(name,mode)         
# cv2.imwrite('t.jpg', img)           ret, buffer = cv2.imencode('.jpg', img)          frame = buffer.tobytes()          yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
        # cap.release()  @app.route('/select')  def select():  
    """video Streaming"""      return render_template('selection.html')  
@app.route('/')  def login():  
    """video Streaming"""      return render_template('login.html')  
@app.route('/in_feed')  def in_feed():  
    """Video streaming route. Put this in the src attribute of an img tag."""     return  	Response(in_gen(),mimetype='multipart/x-mixed-replace; boundary=frame') 
@app.route('/out_feed')  def out_feed():  
    """Video streaming route. Put this in the src attribute of an img tag."""      return  	Response(out_gen(),mimetype='multipart/x-mixed-replace; boundary=frame')  @app.route('/in')  def inhtml():  
    """video Streaming"""      return render_template('in.html')  
@app.route('/out')  def outhtml():  
    """video Streaming"""      return render_template('out.html')  if __name__ == '__main__':      app.run(debug=True,host='0.0.0.0', port=5000)  

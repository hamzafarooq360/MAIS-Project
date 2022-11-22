import cv2
from model import FacialExpressionModel
import numpy as np

# used to detect faces in a picture
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#create model
model = FacialExpressionModel("model.json", "model_weights.h5")
#choose font
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    
    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]
            
            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            #put text and rectangles
            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            #add emojis based on emotion
            img = cv2.imread(f"static/images/emotions/{pred}.png")
            img = cv2.resize(img, (100,100))
            fr[100:200, :100] = cv2.addWeighted(fr[100:200, :100], 0, img, 1, 0)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:44:06 2017

@author: davidpvilaca
"""

import cv2

def detectFaceAndEyes(img):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.4, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    return img

    
    

img1 = detectFaceAndEyes(cv2.imread('img1.jpg'))
img2 = detectFaceAndEyes(cv2.imread('img2.jpg'))
img3 = detectFaceAndEyes(cv2.imread('img3.jpg'))
img4 = detectFaceAndEyes(cv2.imread('img4.jpg'))

cv2.imwrite('img1_saida.jpg', img1)
cv2.imwrite('img2_saida.jpg', img2)
cv2.imwrite('img3_saida.jpg', img3)
cv2.imwrite('img4_saida.jpg', img4)
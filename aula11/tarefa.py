#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 09:17:06 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import cv2
import math
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def loadImg(path):
    img = cv2.imread(path)
    return (img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

def detectFaces(gray):
    return face_cascade.detectMultiScale(gray, 1.3, 5)

def detectEyes(img, gray, faces):
    arrEyes = []
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        arrEyes.append({
            "roi_gray": roi_gray,
            "roi_color": roi_color,
            "eyes": eyes
        })
    return arrEyes

def getColor(hsvIndex):
    if (hsvIndex >= 0 and hsvIndex <= 10):
        return "Escuro"
    elif (hsvIndex > 10 and hsvIndex <= 35):
        return "Claro"
    else:
        return "Escuro"
    


paths = ["cor1.jpg","cor2.jpg","cor3.jpg","cor4.jpg","cor5.jpg","cor6.jpg","cor7.png"]

for path in paths:
    img, gray = loadImg(path)
    faces = detectFaces(gray)
    eyes = detectEyes(img, gray, faces)

    for e in eyes:
        maxs = []
        for (ex,ey,ew,eh) in e["eyes"]:
            #cv2.rectangle(e["roi_color"],(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            eyeCrop = e["roi_color"][ey:ey+eh, ex:ex+eh]
            eyeCentr = eyeCrop[math.ceil(len(eyeCrop[0]) / 3):math.ceil(len(eyeCrop[0]) / 3) * 2, math.ceil(len(eyeCrop[1]) / 3):math.ceil(len(eyeCrop[1]) / 3) * 2]
            eyeCentrHsv = cv2.cvtColor(eyeCentr, cv2.COLOR_BGR2HSV)
            hist,bins = np.histogram(eyeCentrHsv.ravel(), bins=45)
            maxs.append(hist.argmax())
            #plt.imshow(cv2.cvtColor(eyeCentr, cv2.COLOR_BGR2RGB))
            #plt.plot(hist, color='r')
            #plt.subplot('122')
        plt.figure()
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(getColor(np.average(maxs)))

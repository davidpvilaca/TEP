#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 08:27:08 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

def gaussianBlur(img, value = (35, 35)):
    return cv2.GaussianBlur(img, value, 0)

def threshold(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

def getContours(img):
    return cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]

img = cv2.imread('mao1.jpg')
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = threshold( gaussianBlur(img_g) )
contours = getContours(thresh)
cnt = max(contours, key = lambda x: cv2.contourArea(x))

res = img.copy()
# draw contours
#cv2.drawContours(res, [cnt], 0, (0, 255, 0), 0)

hull = cv2.convexHull(cnt)
# draw contours
#cv2.drawContours(res, [hull], 0,(0, 0, 255), 0)

moments = cv2.moments(cnt)
if moments['m00']!=0:
    cx = int(moments['m10']/moments['m00'])
    cy = int(moments['m01']/moments['m00'])

centr = (cx,cy)

# circle
cv2.circle(res,centr,10,[0,0,255],2)


hull2 = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull2)

points = []

def addPoints(point):
    add = True
    for p in points:
        if (abs(p[0] - point[0]) <= 50 and abs(p[1] - point[1]) <= 50):
            add = False
    if (add):
        points.append(point)

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(res,start, end, [0,255,0], 2)
    if (math.sqrt( ((centr[0]-far[0])**2) + ((centr[1]-far[1])**2) ) > 150 and far[1] < centr[1]):
        cv2.circle(res,far,6,[0,0,0],-1)
        addPoints(far)
            

# show image
#plt.imshow(res, cmap=plt.cm.Greys_r)
plt.imshow( cv2.cvtColor(res, cv2.COLOR_BGR2RGB) )
plt.title(str(len(points)) + " dedos")


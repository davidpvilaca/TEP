#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 09:24:34 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2

img_modelo = cv2.imread('placas_modelo.jpg')
img_modeloG = cv2.cvtColor(img_modelo.copy(), cv2.COLOR_BGR2GRAY)
qtd_circles = 1

img_find = cv2.imread('teste1.jpg')
img_findG = cv2.cvtColor(img_find.copy(), cv2.COLOR_BGR2GRAY)

len_circle = 0
minDist = 0
find_red = img_find[:,:,2]
# get circles
while len_circle != qtd_circles or minDist < 1:
    minDist += 1
    circles = cv2.HoughCircles(find_red,cv2.HOUGH_GRADIENT,1,minDist)
    circles = np.uint16(np.around(circles))
    len_circle = circles.shape[1]

templates = []
for i in circles[0,:]:
    x = i[1]
    y = i[0]
    r = i[2]
    templates.append(cv2.resize(img_findG[x-r:x+r, y-r:y+r], (60,60)))


for template in templates:
    
    w, h = template.shape[::-1]

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    
    for meth in methods:
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img_modeloG,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img_modelo,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(cv2.cvtColor(img_modelo, cv2.COLOR_BGR2RGB),cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()


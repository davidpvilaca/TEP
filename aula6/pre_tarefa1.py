#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 08:30:23 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

pratos = cv2.imread('teste1.jpg')
cimg = pratos.copy()
gray = cv2.cvtColor(pratos,cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(pratos[:,:,2],cv2.HOUGH_GRADIENT,1,1)
circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    # desenha circulo
    cv2.circle(cimg, (i[0],i[1]),i[2],(0,255,0),2)
    # desenha o centro do círculo
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

plt.imshow(cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB))
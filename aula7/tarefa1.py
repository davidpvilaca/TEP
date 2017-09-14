#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 08:29:23 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import cv2

img1 = cv2.imread('vermelho3.jpg')


img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

i = img1_hsv[:,:, 0] < 30
img1_hsv[i, 0] += 30
i = img1_hsv[:,:, 0] > 150
img1_hsv[i, 0] -= 150

img_saida = cv2.cvtColor(img1_hsv, cv2.COLOR_HSV2BGR)

plt.subplot(121), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.subplot(122), plt.imshow(cv2.cvtColor(img_saida, cv2.COLOR_BGR2RGB))
plt.title('Saída')

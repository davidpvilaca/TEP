#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 23:19:06 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy.ndimage import label

def loadImg(path):
    img = cv2.imread(path)
    return (img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

def binOtsu(img_gray):
    img_bin = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int))
    return img_bin

def showImg(img, cmap=None):
    plt.figure()
    plt.imshow(img, cmap=cmap)
    
"""
@param {} a
@param {cv2 image} img
"""
def segment_on_dt(a, img):
    border = cv2.dilate(img, None, iterations=5)
    border = border - cv2.erode(border, None)
    cv2.imwrite('result1.png', border)
    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)    
    lbl, ncc = label(dt)
    cv2.imwrite('result2.png', lbl)
    contours1 = cv2.findContours(lbl.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
    lbl = lbl * (255/ncc)
    lbl[border == 255] = 255
    cv2.imwrite('result3.png', lbl)
    lbl = lbl.astype(np.int32)
    cv2.watershed(a, lbl)
    cv2.imwrite('result4.png', lbl)
    lbl[lbl == -1] = 0

    lbl = lbl.astype(np.uint8)
    seg = 255 - lbl
    
    showImg(seg, plt.cm.Greys_r)
    contours2 = cv2.findContours(seg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

    return seg, np.max([len(contours1), len(contours2)])


def main():
    
    paths = ['laranjas.jpg', 'ovos.jpg', 'patologia1.jpg', 'aspirina.jpg']
    #paths = ['patologia1.jpg']
    
    for path in paths:
        img, gray = loadImg(path)
        result, num = segment_on_dt(img.copy(), binOtsu(gray))    
        #showImg(binOtsu(gray), plt.cm.Greys_r)
        showImg(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(str(num))
    
    return 0

if __name__ == '__main__':
    main()
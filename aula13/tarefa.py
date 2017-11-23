#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 00:14:59 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np
import scipy
from scipy import ndimage
from skimage import measure


def showImg(img, gray=False):
    plt.figure()
    cmap = None
    if (gray):
        cmap = plt.cm.Greys_r
    plt.imshow(img, cmap=cmap)
    return

def loadImg(path):
    img = cv2.imread(path)
    return (img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

def bgr2Rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def binOtsu(img_gray):
    img_bin = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    #img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int))
    return img_bin


maze = loadImg('maze20_1.png')[1]
binMaze = binOtsu(maze)

scipy.sparse.csgraph.connected_components(binMaze)

showImg(binMaze, True)
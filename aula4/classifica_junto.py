#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:21:45 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2

def getHist(arr_img):
    hists = []
    sm = []
    for img in arr_img:
        hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hists.append(hist)
        sm.append(np.average(hist[:]))
    
    return 

def compareHist(hist1, hist2):
    OPENCV_METHODS = ( ("Correlation", cv2.HISTCMP_CORREL), ("Intersection", cv2.HISTCMP_INTERSECT) )    
    return cv2.compareHist(hist1, hist2, OPENCV_METHODS[0][1]) # intersec

def showImages(imgArr, titleArr):
    lenImgArr = len(imgArr)
    assert lenImgArr == len(titleArr)
    plt.figure(figsize = (8,8))
    p = int(str(lenImgArr//2) + "20" if lenImgArr > 2 and ( (lenImgArr % 2) == 0 ) else str(lenImgArr//3) + "30")
    i = 0
    for img in imgArr:
        plt.subplot(p + i + 1)
        plt.title(titleArr[i])
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        i = i + 1


def main():
    
    imageSource = {
        'Goblin Town': {
            'images': [
                cv2.imread('Goblin_town1.jpg'),
                cv2.imread('Goblin_town2.jpg'),
                cv2.imread('Goblin_town3.jpg'),
                cv2.imread('Goblin_town4.jpg')
            ],
            'hist': None
        },
        'Mordor': {
            'images': [
                cv2.imread('mordor1.jpg'),
                cv2.imread('mordor2.jpg'),
                cv2.imread('Mordor3.jpg'),
                cv2.imread('Mordor4.jpg')
            ],
            'hist': None
        },
        'Rivendell': {
            'images': [
                cv2.imread('Rivendell1.jpg'),
                cv2.imread('Rivendell2.jpg'),
                cv2.imread('Rivendell3.jpg'),
                cv2.imread('Rivendell4.jpg')
            ],
            'hist': None
        },
        'Shire': {
            'images': [
                cv2.imread('Shire1.jpg'),
                cv2.imread('Shire2.jpg'),
                cv2.imread('Shire3.jpg'),
                cv2.imread('Shire4.jpg')
            ],
            'hist': None
        }
    }
    
    # calc histogram
    for name,data in imageSource.items():
        imageSource[name]['hist'] = getHist(imageSource[name]['images'])
    
    imagesOnde = [
        cv2.imread('Onde1.jpg'),
        cv2.imread('Onde2.jpg'),
        cv2.imread('Onde3.jpg'),
        cv2.imread('Onde4.jpg')
    ]
    
    imgs,titles = [],[]
    i = 1
    for ondeImg in imagesOnde:
        ondeHist = getHist([ondeImg])
        results = []
        for imgSrcName, srcData in imageSource.items():
            results.append((compareHist(ondeHist, srcData['hist']), imgSrcName))
        result = sorted(results, reverse = True)[0]
        imgs.append(ondeImg)
        titles.append(result[1] + " (" + "Onde" + str(i) + ")")
        i += 1
    showImages(imgs, titles)
    plt.show()
    
    return 0

if __name__ == '__main__':
    main()
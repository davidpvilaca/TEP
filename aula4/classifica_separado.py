#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:42:40 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

pathImages = {
    'Globin Town': [
        'Goblin_town1.jpg',
        'Goblin_town2.jpg',
        'Goblin_town3.jpg',
        'Goblin_town4.jpg'
    ],
    'Mordor': [
        'mordor1.jpg',
        'mordor2.jpg',
        'Mordor3.jpg',
        'Mordor4.jpg'
    ],
    'Rivendell': [
        'Rivendell1.jpg',
        'Rivendell2.jpg',
        'Rivendell3.jpg',
        'Rivendell4.jpg',
    ],
    'Shire': [
        'Shire1.jpg',
        'Shire2.jpg',
        'Shire3.jpg',
        'Shire4.jpg'
    ]
}
# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves
index = {}
images = {}

ondeArr = []

# Carregando imagens "Onde"
for i in range(1,5):
    imgOnde = cv2.imread('Onde'+str(i)+'.jpg')
    imgOndeRGB = cv2.cvtColor(imgOnde, cv2.COLOR_BGR2RGB)
    histOnde = cv2.calcHist([imgOnde], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
    histOnde = cv2.normalize(histOnde, histOnde).flatten()
    ondeArr.append({ 'image': imgOndeRGB, 'hist': histOnde, 'name': 'Onde'+str(i) })
# fim carregamento onde

# Carregando imagens de comparação
for (name, imagePaths) in pathImages.items():
    index[name] = []
    images[name] = []
    
    for path in imagePaths:
        image = cv2.imread(path)
        images[name].append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        index[name].append(hist)

# fim carregamento comparações

methodResult = {}


OPENCV_METHODS = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Intersection", cv2.HISTCMP_INTERSECT))

for (methodName, method) in OPENCV_METHODS:
    results = {}
    methodResult[methodName] = {}
    
    for onde in ondeArr:
        imageOnde = onde['image']
        histOnde = onde['hist']
        nameOnde = onde['name']
        methodResult[methodName][nameOnde] = {}
        
        for (name, hists) in index.items():
            results[name] = []
            for hist in hists:
                #print('Comparando "'+name+'" com "Onde'+ str(onde['name'])+'.jpg" com método "'+methodName+'"')
                d = cv2.compareHist(histOnde, hist, method)
                results[name].append(d)
            #print('Resultado "'+name+'" para "Onde'+ str(onde['name'])+'.jpg" é '+str(results[name]))
            methodResult[methodName][nameOnde][name] = np.max(results[name])
        #print("\n\n\n=======================\n\n\n")
    

i = 1
for (methodName, results) in methodResult.items():
    figure = plt.figure(figsize = (8,8))
    figure.text(0, 1, methodName)
    for (ondeName, ondeResults) in results.items():
        result = sorted([(v, k) for (k, v) in ondeResults.items()], reverse = True)[0]
        #print(ondeName + ': ' + str(result[1]) + ', segundo ' + methodName)
        plt.subplot(220 + i)
        plt.title(methodName)
        plt.imshow(ondeArr[int(ondeName[-1])-1]['image'])
        plt.title(result[1] + ' ('+ondeName+')')
        i = i + 1 if i < 4 else 1
    plt.show()
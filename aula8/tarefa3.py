#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:40:38 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (0, 1, 0, 0, 1, 0, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 0, 1, 0, 1, 0, 0): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}


def main():
    
    img = cv2.imread('ex2.png', cv2.IMREAD_GRAYSCALE)
    
    thresh1 = cv2.threshold(img, 0, 255,	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh2 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel) # abertura
    closing = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel) # fechamento
    
    #plt.imshow(thresh2, cmap=plt.cm.Greys_r)
    
    
    cnts1 = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts1[1]
    digitCnts = []
    
    # loop over the digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if w >= 10 and (h >= 3):
            digitCnts.append(c)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    #plt.imshow(img, cmap=plt.cm.Greys_r)
    
    digits = []
    
    # loop over each of the digits
    for c in digitCnts:
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        roi = thresh2[y:y + h, x:x + w]
        # compute the width and height of each of the 7 segments
        (roiH, roiW) = roi.shape
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
        dHC = int(roiH * 0.05)
        digits.append(roi)
        segments = [((0, 0), (w, dH)),	# top
                    ((0, 0), (dW, h // 2)),	# top-left
                    ((w - dW, 0), (w, h // 2)),	# top-right
                    ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
                    ((0, h // 2), (dW, h)),	# bottom-left
                    ((w - dW, h // 2), (w, h)),	# bottom-right
                    ((0, h - dH), (w, h))	# bottom
                    ]
        on = [0] * len(segments)
        # loop over the segments
        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            segROI = roi[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)
            # if the total number of non-zero pixels is greater than
            # 50% of the area, mark the segment as "on"
            if total / float(area) > 0.5:
                on[i]= 1
        # lookup the digit and draw it on the image
        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)
        print(tuple(on))
        print(digit)
        
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(img, str(digit), (x, y +20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
    plt.imshow(img, cmap=plt.cm.Greys_r)
    
    return 0


if __name__ == '__main__':
    main()

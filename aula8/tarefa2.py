#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 23:21:28 2017

@author: davidpvilaca
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2

DIGITS_LOOKUP = {
    #0  1  2  3  4  5  6
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (0, 1, 0, 0, 1, 0, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (1, 0, 0, 1, 0, 0, 1): 3,
    (1, 0, 1, 1, 0, 0, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 0, 1, 0, 0, 0, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
    (1, 1, 1, 1, 0, 1, 0): 9
}

def segmentDigits(path, typeThresh = cv2.THRESH_BINARY):
    
    img_o = cv2.imread(path)
    img = cv2.cvtColor(img_o.copy(), cv2.COLOR_BGR2GRAY)
    
    thresh1 = cv2.threshold(img, 0, 255,	typeThresh + cv2.THRESH_OTSU)[1]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh2 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel) # abertura
    closing = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel) # fechamento
    
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
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
    rois_w_avg = 0
    
    # loop over each of the digits
    for c in digitCnts:
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        roi = thresh2[y:y + h, x:x + w]
        
        #plt.figure()
        #plt.imshow(roi, cmap=plt.cm.Greys_r)
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
            if (total / float(area)) >= 0.4:
                on[i]= 1
        # lookup the digit and draw it on the image
        lookup = tuple(on)
        digit = DIGITS_LOOKUP[lookup] if lookup in DIGITS_LOOKUP else ''
        if ( rois_w_avg != 0 and (w/rois_w_avg) < 0.5 ):
            digit = 1
        else:
            rois_w_avg = h if rois_w_avg == 0 else np.average([rois_w_avg, w])
        digits.append(digit)
        
        #print(str(lookup) + ': ' + str(digit))
        
        #print(tuple(on))
        #print(digit)
        
        cv2.rectangle(img_o, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(img_o, str(digit), (x, y +20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
    plt.figure()
    plt.imshow(cv2.cvtColor(img_o, cv2.COLOR_BGR2RGB))
    


def main():
    
    inputs = [ 
        { 'path': 'ex.png', 'type': cv2.THRESH_BINARY_INV },
        { 'path': 'ex2.png', 'type': cv2.THRESH_BINARY },
        { 'path': 'ex3.png', 'type': cv2.THRESH_BINARY }
    ]
    
    for i in inputs:
        segmentDigits(i['path'], i['type'])
    
    return 0


if __name__ == '__main__':
    main()

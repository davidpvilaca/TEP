#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:32:20 2017

@author: davidpvilaca
"""
#import matplotlib.pyplot as plt
#import numpy as np
import cv2



def main():
    
    img = cv2.imread('ex.png', cv2.IMREAD_GRAYSCALE)
    
    thresh1 = cv2.threshold(img, 0, 255,	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh2 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel) # abertura
    closing = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel) # fechamento
    
    cv2.imwrite('result1.png', thresh1)
    cv2.imwrite('result2.png', thresh2)
    cv2.imwrite('result3.png', closing)
    
    return 0


if __name__ == '__main__':
    main()

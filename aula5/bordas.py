#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 07:35:47 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    
    return False

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def isValidIntersec(r, lim):
    return r[0] > 0 and r[0] <= lim[0] and r[1] > 0 and r[1] <= lim[1]


def main():
    
    imgEntrada = cv2.imread('entrada.jpg')
    shapeEntrada = imgEntrada.shape
    imgGrayEntrada = cv2.cvtColor(imgEntrada,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(imgGrayEntrada,50,150,apertureSize = 3)
    cv2.imwrite('saida.jpg', edges)
    
    
    LIMITE = 0
    lines = cv2.HoughLines(edges,1,np.pi/180, LIMITE)
    
    s1, s2, s3 = lines.shape
    
    while s1 != 4:
        LIMITE += 1
        lines = cv2.HoughLines(edges,1,np.pi/180, LIMITE)
        s1, s2, s3 = lines.shape
        
    L = []
    
    for i in range(s1):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        L.append(line([y1,x1], [y2,x2]))
        cv2.line(imgEntrada,(x1,y1),(x2,y2),(0,0,255),1)
    
    
    intersec = []
    for i in range(len(L)):
        for j in range(i):
            r = intersection(L[i], L[j])
            if (isValidIntersec(r, shapeEntrada)):
                intersec.append(r)
    
    src = np.array(intersec, dtype = "float32")
    dst = np.array([
		[0, 0],
		[shapeEntrada[0] - 1, 0],
		[shapeEntrada[0] - 1, shapeEntrada[1] - 1],
		[0, shapeEntrada[1] - 1]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(src, dst)
    cv2.warpPerspective(imgEntrada, M, (400, 300))
    
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(imgEntrada, cv2.COLOR_BGR2RGB))
    plt.title('Input')
    plt.subplot(122)
    plt.imshow(edges, cmap=plt.cm.Greys_r)
    plt.title('Output')
    plt.show()
    
    return 0

if __name__ == '__main__':
    main()

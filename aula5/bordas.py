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
        return (y, x)
    
    return False

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def isValidIntersec(r, lim):
    return r[0] > 0 and r[0] <= lim[0] and r[1] > 0 and r[1] <= lim[1]

def four_point_transform(image, pts):
    	# obtain a consistent order of the points and unpack them
    	# individually
    rect = order_points(pts)
    #print(pts)
    print(rect)
    (tl, tr, br, bl) = rect
    
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
     
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
    		[0, 0],
    		[maxWidth - 1, 0],
    		[maxWidth - 1, maxHeight - 1],
    		[0, maxHeight - 1]], dtype = "float32")
     
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
     
    # return the warped image
    return warped

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect

def main():
    
    imgEntrada = cv2.imread('entrada.jpg')
    shapeEntrada = imgEntrada.shape
    imgGrayEntrada = cv2.cvtColor(imgEntrada,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(imgGrayEntrada,50,150,apertureSize = 3)
    
    
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
        #cv2.line(imgEntrada,(x1,y1),(x2,y2),(0,0,255),1)
    
    
    intersec = []
    for i in range(len(L)):
        for j in range(i):
            r = intersection(L[i], L[j])
            if (isValidIntersec(r, shapeEntrada)):
                intersec.append(r)
    xy1 = (int(intersec[0][0]), int(intersec[0][1]))
    xy2 = (int(intersec[1][0]), int(intersec[1][1]))
    
    
    pts = np.array(intersec, dtype = "float32")
    warped = four_point_transform(imgEntrada, pts)
    
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(imgEntrada, cv2.COLOR_BGR2RGB))
    plt.title('Input')
    plt.subplot(122)
    plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    plt.title('Output')
    plt.show()
    
    cv2.imwrite('saida.jpg', warped)
    
    return 0

if __name__ == '__main__':
    main()

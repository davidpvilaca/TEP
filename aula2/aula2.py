#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 07:47:56 2017

@author: davidpvilaca
"""

import matplotlib.pyplot as plt
# import numpy as np

field = plt.imread('field.png')

# separando canais rgb

red = field[:, :, 0]
green = field[:, :, 1]
blue = field[:, :, 2]

# escala de cinza

gs1 = (field[:, :, 0] + field[:, :, 1] + field[:, :, 2]) / 3 # média simples
gs2 = (0.299 * field[:, :, 0]) + (0.587 * field[:, :, 1]) + (0.114 * field[:, :, 2]) # ponderada

# histograma

plt.hist(field[:,:,0].ravel(), 256, [0, 1], color='r')
plt.hist(field[:,:,1].ravel(), 256, [0, 1], color='g')
plt.hist(field[:,:,2].ravel(), 256, [0, 1], color='b')

"""
 Iluminação, ruído e detecção de bordas
"""

lena = plt.imread('lena.bmp')

lenac = lena + 30

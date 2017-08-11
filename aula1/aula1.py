# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
import matplotlib.pyplot as plt
import numpy as np
f = plt.imread('field.png')
plt.imshow(f)

# red
r = f.copy()
plt.imshow(r)
r[:,:,1] = 0
r[:,:,2] = 0
plt.imshow(r)

# green
g = f.copy()
g[:,:,0] = 0
g[:,:,2] = 0
plt.imshow(g)

# blue
b = f.copy()
b[:,:,0] = 0
b[:,:,1] = 0
plt.imshow(b)
plt.imshow(f)

# grayscale
gs1 = (f[:,:,0] + f[:,:,1] + f[:,:,2]) / 3
plt.imshow(gs1)
plt.imshow(gs1, cmap=plt.cm.Greys_r)
plt.imshow(f)

gs2 = 0.299*f[:,:,0] + 0.587*f[:,:,1] + 0.114*f[:,:,2]
plt.imshow(gs2, cmap=plt.cm.Greys_r)
plt.imshow(f)

h = f.copy()
plt.imshow(h)
idx = h[:,:,1] > 0.5
idx.shape
h[idx,1] = 0
plt.imshow(h)

h = f.copy()
idx = h[:,:,1] > h[:,:,0]
h[idx,1] = 0
plt.imshow(h)

h.shape
plt.imshow(f)

# histograma
plt.imshow(b)
plt.hist(b.ravel(), 256, [0, 1])
plt.hist(f[:,:,2].ravel(), 256, [0, 1])

plt.hist(f[:,:,0].ravel(), 256, [0, 1])
plt.hist(f[:,:,1].ravel(), 256, [0, 1])
plt.hist(f[:,:,2].ravel(), 256, [0, 1])

plt.hist(f[:,:,0].ravel(), 256, [0, 1], color='r')
plt.hist(f[:,:,1].ravel(), 256, [0, 1], color='g')
plt.hist(f[:,:,2].ravel(), 256, [0, 1], color='b')

plt.hist(gs2.ravel(), 256, [0, 1])
hs,bins = np.histogram(gs2, bins=256)
plt.plot(hs)
plt.hist(gs2.ravel(), 256, [0, 1])

hr,bins = np.histogram(f[:,:,0], bins=256)
hg,bins = np.histogram(f[:,:,1], bins=256)
hb,bins = np.histogram(f[:,:,2], bins=256)
plt.plot(hr, color='r')
plt.plot(hg, color='g')
plt.plot(hb, color='b')

nf = 1 - f
plt.imshow(nf)

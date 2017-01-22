import cv2
import numpy as np
import random

canvas = cv2.imread('./Blank.jpg')
sizeX = canvas.shape[0]
sizeY = canvas.shape[1]
canvas = cv2.imread('../Carrier.jpg')

channel = 1
lineWidth = 1

for i in range(sizeX):
    c = 1
    while c * c < sizeY:
        j = c * c
        canvas[i,j,channel] = 255        
        c += 1    

#with open('lossless.txt','w') as f:
#    f.write(str(list(canvas)))

cv2.imwrite('./Stripes.png',canvas)
cv2.imwrite('./Stripes.jpg',canvas,[cv2.IMWRITE_JPEG_QUALITY, 100])

lossy = cv2.imread('./Stripes.jpg')

#with open('lossy.txt','w') as f:
#    f.write(str(list(lossy)))

reconstruct = cv2.imread('./Blank.jpg')

for i in range(0,sizeX):
    for j in range(0,sizeY):
        m = max(lossy[i,j])
        c = np.argmax(lossy[i,j])
        reconstruct[i,j,c] = m

cv2.imwrite('./ReconstructedStripes.png',reconstruct)        










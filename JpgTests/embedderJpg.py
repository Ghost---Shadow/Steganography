import cv2
import numpy as np
import random

canvas = cv2.imread('./Blank.jpg')
step = 8
shift = 3
def runPass(img):
    sizeX = img.shape[0]
    sizeY = img.shape[1]

    channel = 1 #0
    
    boxSize = 1
    for i in range(0,sizeX,step):
        for j in range(0,sizeY,step):
            '''
            for i1 in range(i-boxSize,i+boxSize):
                for j1 in range(j-boxSize,j+boxSize):
                    canvas[i1,j1,channel] = 255'''
            val = (int(i/step) >> 1) << shift
            #print(val)

            img[i,j,channel] = val
                    
            #channel = (channel + 1) % 3
passes = 1
for i in range(passes):    
    runPass(canvas)
    #cv2.imwrite('./Dots.png',canvas)
    cv2.imwrite('./Dots.jpg',canvas)
    canvas = cv2.imread('./Dots.jpg')

#with open('lossless.txt','w') as f:
#    f.write(str(list(canvas)))

#cv2.imwrite('./Dots.png',canvas)
#cv2.imwrite('./Dots.jpg',canvas)

lossy = cv2.imread('./Dots.jpg')

#with open('lossy.txt','w') as f:
#    f.write(str(list(lossy)))

reconstruct = cv2.imread('./Blank.jpg')
sizeX = reconstruct.shape[0]
sizeY = reconstruct.shape[1]
c = 1 #0
for i in range(0,sizeX,step):
    for j in range(0,sizeY,step):
        reconstruct[i,j,c] = lossy[i,j,c] << (8 - shift - 2)
        #c = (c + 1) % 3     

cv2.imwrite('./ReconstructedDots.png',reconstruct)
#cv2.imshow('./ReconstructedDots.png',reconstruct)  










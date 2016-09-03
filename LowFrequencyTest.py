import cv2
import numpy as np

amplitude = 10
omega = 255

img = cv2.imread('./Carrier.jpg')

sizeX = img.shape[1]
sizeY = img.shape[0]

x = np.sin([i*i for i in range(sizeX)])
x = list(np.uint8(((x*omega + 1.0)/2.0)*amplitude))
#x = list(np.uint8(((x + 1.0)/2.0)*255))

mask = np.array([[[i,i,i] for i in x] for _ in range(sizeY)])

#cv2.imshow('mask',mask)

img = cv2.add(img,mask)

cv2.imshow('img',img)




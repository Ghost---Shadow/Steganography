import cv2
import numpy as np

canvas = cv2.imread('../FingerPrint.png')
mask = 192
canvas = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
canvas = np.bitwise_and(canvas,mask)
cv2.imwrite('./Expected.png',canvas)

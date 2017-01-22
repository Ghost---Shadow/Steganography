import numpy as np
import cv2
import matplotlib.pyplot as plt

PASS_COUNT = 8
FILE_NAME = './Passes/Checkerboard64_'
EXTENSION = '.jpg'

shift = 3
mask = 1 << shift
crop = 3

def runPass(canvas,p):
    sizeX = canvas.shape[0]
    sizeY = canvas.shape[1]   

    shape = [[1 if (i + j) % 2 == 0 else 0 for j in range(8)] for i in range(8)]
    shape = np.array(shape)
    shape *= mask
    #print(shape)

    def fillBlock(img,x,y,c):
        for i in range(x,x+8,1):
            for j in range(y,y+8,1):
                img[i,j] &= (255 - mask)
                img[i,j] |= c

    for i in range(8):
        for j in range(8):
            fillBlock(canvas,i*8,j*8,shape[i,j])

    #cv2.imwrite('Checkerboard64.png',canvas)        
    cv2.imwrite(FILE_NAME+str(p)+EXTENSION,canvas)

#lossy = cv2.imread('./Blank64.png')
lossy = cv2.imread('./Image64.png')
lossy = cv2.cvtColor(lossy,cv2.COLOR_BGR2GRAY)

sizeX = lossy.shape[0]
sizeY = lossy.shape[1]

for i in range(PASS_COUNT):
    runPass(lossy,i)
    lossy = cv2.imread(FILE_NAME+str(i)+EXTENSION)
    lossy = cv2.cvtColor(lossy,cv2.COLOR_BGR2GRAY)
    plane = (lossy & mask) << 7 - shift
    #plane = cv2.medianBlur(plane,3)
    cv2.imwrite(FILE_NAME+str(i)+'_extract'+EXTENSION,plane)
    
'''print(lossy[0,8+crop:24+crop] & mask)

cv2.imwrite('Checkerboard64_Cropped.jpg',canvas[crop:-crop,crop:-crop])
lossy = cv2.imread('Checkerboard64_Cropped.jpg')
lossy = cv2.cvtColor(lossy,cv2.COLOR_BGR2GRAY)
print(lossy[0,8:24] & mask)'''
'''
x = [i for i in range(sizeX-8)]
y = []
dy = [0]
ddy = [0]

for i in x:
    window = lossy[0,i:i+8] & mask
    y.append(np.mean(window))
    if i > 0:
        dy.append(y[-1] - y [-2])
    if i > 1:
        ddy.append(dy[-1] - dy [-2])
    #print(i,window,np.mean(window))

ddy.append(0)

plt.plot(x,y)
#plt.plot(x,dy)
plt.plot(x,ddy)
plt.show()
'''




        

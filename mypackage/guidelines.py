import cv2
import numpy as np

# OpenCV channels
BLUE = 0
GREEN = 1
RED = 2

# Set N LSBs to 0 for all pixels
def washBitDepth(img,mask):
    return np.bitwise_and(img,mask)

# Generate the lines
def generateGuideLines(img,value = 255):
    SIZE_X = img.shape[0]
    SIZE_Y = img.shape[1]
    CHANNELS = img.shape[2] # Unused

    def verticalLines():
        for i in range(SIZE_X):
            # Blue lines from left
            # Red lines from right
            c = 1
            while c * c < SIZE_Y:
                j = c * c
                img[i][j][BLUE] |= value        
                img[i][SIZE_Y-j-1][RED] |= value
                c += 1
            
            # Green lines from middle
            c = 1
            half = int(SIZE_Y/2)
            while c * c < SIZE_Y / 2:
                j = c * c
                #img[i][half-j][GREEN] |= value
                #img[i][half+j][GREEN] |= value
                c += 1
            
                
    def horizontalLines():
        for j in range(SIZE_Y):
            # Blue lines from top
            # Red lines from bottom
            c = 1
            while c * c < SIZE_X:
                i = c * c
                img[i][j][BLUE] |= value        
                img[SIZE_X-i-1][j][RED] |= value
                c += 1
            
            # Green lines from middle
            c = 1
            half = int(SIZE_X/2)
            while c * c < SIZE_X / 2:
                i = c * c
                #img[half-i][j][GREEN] |= value
                #img[half+i][j][GREEN] |= value
                c += 1            

    verticalLines()
    horizontalLines()

    return img

def getMargins(im,mask = 255):
    im = np.bitwise_and(im,mask)
    def getUpperLeftCorner(im):
        SIZE_X = im.shape[0]
        SIZE_Y = im.shape[1]
        lastPos = -1
        diff = -1
        j = 1
        # Avoid vertical lines
        while im[1,j] > 0 and im[2,j] > 0:
            j += 1
            if j == SIZE_Y:
                return -1

        # Get all the estimates
        estimates = []
        for i in range(SIZE_X):
            if(im[i,j] > 0): 
                if lastPos is not -1:
                    diff = i - lastPos
                    estimatedi = int((diff+1)/2) ** 2
                    estimates.append(estimatedi-i)
                lastPos = i
        # Find modal estimate
        mode = -1
        if len(estimates) > 0:
            mode = (max(set(estimates), key=estimates.count))        
        return mode

    margins = [-1,-1,-1,-1]

    # Left
    margins[0] = getUpperLeftCorner(img[:,:,BLUE])
    # Bottom
    margins[1] = getUpperLeftCorner(np.rot90(img[:,:,RED],1))
    # Right
    margins[2] = getUpperLeftCorner(np.rot90(img[:,:,RED],2))
    # Top
    margins[3] = getUpperLeftCorner(np.rot90(img[:,:,BLUE],3))

    return (margins)

OUTPUT_FILE = 'out.png'
MASK = 1
#img = np.zeros((388,620,3),dtype=np.uint8)
img = cv2.imread('../Carrier.png')
img = washBitDepth(img,~MASK)
img = generateGuideLines(img,MASK)

SIZE_X = img.shape[0]
SIZE_Y = img.shape[1]

cv2.imwrite(OUTPUT_FILE,img)

img = cv2.imread(OUTPUT_FILE)

#img = img[40:140,60:160]

cv2.imshow('sds',img)
m = getMargins(img,MASK)

m[1] = SIZE_X - m[1]
m[2] = SIZE_Y - m[2]
print(m)

    







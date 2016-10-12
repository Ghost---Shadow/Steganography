import cv2
import numpy as np

# OpenCV channels
BLUE = 0
GREEN = 1
RED = 2

# Set N LSBs to 0 for all pixels
def washBitDepth(im,mask):
    return np.bitwise_and(im,mask)

# Generate the lines
def generateGuideLines(im,value = 255):
    SIZE_X = im.shape[0]
    SIZE_Y = im.shape[1]
    CHANNELS = im.shape[2] # Unused

    def verticalLines():
        for i in range(SIZE_X):
            # Blue lines from left
            # Red lines from right
            c = 1
            while c * c < SIZE_Y:
                j = c * c
                im[i][j][BLUE] |= value        
                im[i][SIZE_Y-j-1][RED] |= value
                c += 1
            '''
            # Green lines from middle
            c = 1
            half = int(SIZE_Y/2)
            while c * c < SIZE_Y / 2:
                j = c * c
                im[i][half-j][GREEN] |= value
                im[i][half+j][GREEN] |= value
                c += 1'''
            
                
    def horizontalLines():
        for j in range(SIZE_Y):
            # Blue lines from top
            # Red lines from bottom
            c = 1
            while c * c < SIZE_X:
                i = c * c
                im[i][j][BLUE] |= value        
                im[SIZE_X-i-1][j][RED] |= value
                c += 1
            '''
            # Green lines from middle
            c = 1
            half = int(SIZE_X/2)
            while c * c < SIZE_X / 2:
                i = c * c
                im[half-i][j][GREEN] |= value
                im[half+i][j][GREEN] |= value
                c += 1   '''         

    verticalLines()
    horizontalLines()

    return im

def getMargins(im,mask = 255):
    im = np.bitwise_and(im,mask)
    
    def getMargin(im,c):
        SIZE_X = im.shape[0]
        SIZE_Y = im.shape[1]
        lastPos = -1
        diff = -1
        
        j = 0
        # Avoid vertical lines
        while im[0,j] > 0 and im[1,j] > 0:
            j += 1
            if j == SIZE_Y:
                #with open('dump.txt','w') as f:
                #    f.write(str(im.tolist()))
                return -1

        # Get all the estimates
        estimates = []
        #debug = []
        for i in range(SIZE_X):
            if(im[i,j] > 0): 
                if lastPos is not -1:
                    diff = i - lastPos
                    estimatedi = int((diff+1)/2) ** 2
                    estimates.append(estimatedi-i)
                    #debug.append([i,estimatedi,diff])
                lastPos = i
                
        #with open('debug'+str(c)+'.txt','w') as f:
        #    f.write(str(debug))
        
        # Find modal estimate
        mode = -1
        if len(estimates) > 0:
            mode = (max(set(estimates), key=estimates.count))        
        return mode

    margins = [-1,-1,-1,-1]

    # Top
    margins[0] = getMargin(im[:,:,BLUE],'_TOP')
    # Right
    margins[1] = getMargin(np.rot90(im[:,:,RED],1),'_RIGHT')
    # Bottom
    margins[2] = getMargin(np.rot90(im[:,:,RED],2),'_BOTTOM')
    # Left
    margins[3] = getMargin(np.rot90(im[:,:,BLUE],3),'_LEFT')

    return (margins)

def test():
    OUTPUT_FILE = 'out.png'
    MASK = 1
    #img = np.zeros((388,620,3),dtype=np.uint8)
    img = cv2.imread('../Carrier.png')
    img = washBitDepth(img,~MASK)
    img = generateGuideLines(img,MASK)

    SIZE_X = img.shape[0]
    SIZE_Y = img.shape[1]

    #cv2.imwrite(OUTPUT_FILE,img)

    #img = cv2.imread(OUTPUT_FILE)

    img = img[120:240,60:180]

    #cv2.imshow('cropped',img)
    m = getMargins(img,MASK)

    m[1] = SIZE_Y - m[1]
    m[2] = SIZE_X - m[2]
    print(m)
#test()

    







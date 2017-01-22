import cv2
import numpy as np

class GuideLines:
    def __init__(self):        
        # OpenCV channels
        self.BLUE = 0
        self.GREEN = 1
        self.RED = 2
        
        self.TOP = 0
        self.RIGHT = 1
        self.BOTTOM = 2
        self.LEFT = 3

    # Set N LSBs to 0 for all pixels
    def washBitDepth(self,im,mask):
        return np.bitwise_and(im,mask)

    # Generate the lines
    def generateGuideLines(self,im,value = 255):
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
                    im[i][j][self.BLUE] |= value        
                    im[i][SIZE_Y-j-1][self.RED] |= value
                    c += 1
                '''
                # Green lines from middle
                c = 1
                half = int(SIZE_Y/2)
                while c * c < SIZE_Y / 2:
                    j = c * c
                    im[i][half-j][self.GREEN] |= value
                    im[i][half+j][self.GREEN] |= value
                    c += 1'''
                
                    
        def horizontalLines():
            for j in range(SIZE_Y):
                # Blue lines from top
                # Red lines from bottom
                c = 1
                while c * c < SIZE_X:
                    i = c * c
                    im[i][j][self.BLUE] |= value        
                    im[SIZE_X-i-1][j][self.RED] |= value
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

    def getMargins(self,im,mask = 255):
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
        margins[self.TOP] = getMargin(im[:,:,self.BLUE],'_TOP')
        # Right
        margins[self.RIGHT] = getMargin(np.rot90(im[:,:,self.RED],1),'_RIGHT')
        # Bottom
        margins[self.BOTTOM] = getMargin(np.rot90(im[:,:,self.RED],2),'_BOTTOM')
        # Left
        margins[self.LEFT] = getMargin(np.rot90(im[:,:,self.BLUE],3),'_LEFT')

        return (margins)

    def getActualSize(self,cropped,margins):
        width = margins[self.LEFT] + cropped.shape[1] + margins[self.RIGHT]
        height = margins[self.TOP] + cropped.shape[0] + margins[self.BOTTOM]
        return [height,width]

    def marginsToCorners(self,margins):
        start_x = margins[self.TOP]
        start_y = margins[self.LEFT]
        end_x = margins[self.BOTTOM]
        end_y = margins[self.RIGHT]
        
        corners = [[start_y,start_x],
                   [start_x,end_y],
                   [end_y,end_x],
                   [end_x,start_y]]

        return corners

def test():
    OUTPUT_FILE = 'out.png'
    MASK = 255
    guideLines = GuideLines()
    #img = np.zeros((387,620,3),dtype=np.uint8)
    img = cv2.imread('../Carrier.png')
    img = guideLines.washBitDepth(img,~MASK)
    #print(type(img))
    img = guideLines.generateGuideLines(img,MASK)
    #print(type(img))
    
    #SIZE_X = img.shape[0]
    #SIZE_Y = img.shape[1]

    cv2.imwrite(OUTPUT_FILE,img)

    img = cv2.imread(OUTPUT_FILE)

    img = img[100:300,100:600]

    #cv2.imshow('cropped',img)
    m = guideLines.getMargins(img,MASK)
    print(m)

    sizes = guideLines.getActualSize(img,m)
    print(sizes)
    corners = guideLines.marginsToCorners(m)
    print(corners)

    m[1] = sizes[1] - m[1]
    m[2] = sizes[0] - m[2]
    print(m)
#test()

    







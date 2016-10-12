import cv2
import numpy as np
import random

class Extractor:
    def __init__(self,passes,key,mask,shift,logging = False):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        self.MASK = mask
        self.SHIFT = shift
        self.logging = logging

    def extract(self,embedded,CORNERS,ACTUAL_SIZE,BIOMETRIC_SIZE):
        # Extract number of channels
        self.CHANNELS = embedded.shape[2]

        # Count votes
        votes = [[[] for _ in range(BIOMETRIC_SIZE)] for _ in range(BIOMETRIC_SIZE)]

        # Rotation function
        rotateIJ = lambda i,j,orientation:\
            (i,j) if orientation == 0 \
            else rotateIJ(j,-i-1,orientation-1)

        # Seed the PRG
        random.seed(self.KEY)

        # Debug
        self.table = []

        # Size of the input image
        inputSize = [[embedded.shape[0],embedded.shape[1]],
                     [embedded.shape[1],embedded.shape[0]]]

        def runPass(passNumber):
            channel = passNumber % self.CHANNELS
            orientation = (passNumber) % 4
            
            width = ACTUAL_SIZE[passNumber%2][0] - 1
            height = ACTUAL_SIZE[passNumber%2][1] - 1
            
            for i in range(BIOMETRIC_SIZE):
                for j in range(BIOMETRIC_SIZE):
                    # x,y coordinates of original image
                    x = random.randint(0,height) - CORNERS[orientation][1]
                    y = random.randint(0,width) - CORNERS[orientation][0]                   

                    if x < 0 or y < 0:
                        continue

                    # Rotate the coordinates
                    ni,nj = i,j
                    nx,ny = rotateIJ(x,y,orientation)                    

                    try:
                        # Extract the value
                        value = embedded[nx,ny,channel] & self.MASK            

                        # Add votes to the list
                        votes[ni][nj].append(value << self.SHIFT)
                    except:
                        #print(nx,ny)
                        pass

                    # Debug
                    if i == 64 and passNumber == 3 and self.logging:
                        row = [passNumber,ni,nj,nx,ny,value]
                        self.table.append(row)                

        for i in range(self.NUMBER_OF_PASSES):
            runPass(i)
     
        # Output canvas
        canvas = np.zeros((BIOMETRIC_SIZE,BIOMETRIC_SIZE),dtype=np.uint8) + 255  

        # Count votes
        for i in range(BIOMETRIC_SIZE):
            for j in range(BIOMETRIC_SIZE):
                a = votes[i][j]
                if len(a) == 0:
                    continue
                value = max(map(lambda val: (a.count(val), val), set(a)))[1]
                canvas[i,j] = value

        # Debug logs
        if self.logging:
            with open('extract.txt','w') as f:
                f.write(str(self.table))
            with open('votes.txt','w') as f:
                f.write(str(votes))

        return canvas

def test():    
    NUMBER_OF_PASSES = 8
    inputFile = './out'+str(NUMBER_OF_PASSES)+'.png'
    
    ACTUAL_SIZE = [[620,387],[387,620]]

    START_X,END_X = 100,300 # HEIGHT
    START_Y,END_Y = 100,600 # WIDTH

    # WIDTH - HEIGHT
    CORNERS = [[START_Y,START_X],
               [START_X,ACTUAL_SIZE[0][0] - END_Y],
               [ACTUAL_SIZE[0][0] - END_Y,ACTUAL_SIZE[0][1] - END_X],
               [ACTUAL_SIZE[0][1] - END_X,START_Y]]
               
    print(CORNERS)

    KEY = 1234
    CHANNELS = 3
    MASK = 6
    SHIFT = 5
    BIOMETRIC_SIZE = 128

    extractor = Extractor(NUMBER_OF_PASSES,KEY,MASK,SHIFT,False)
    
    embedded = cv2.imread(inputFile)
    embedded = embedded[START_X:END_X,START_Y:END_Y]
    cv2.imshow('cropped',embedded)
    
    biometric = extractor.extract(embedded,CORNERS,ACTUAL_SIZE,BIOMETRIC_SIZE)
    
    cv2.imwrite('extract.png',biometric)
    cv2.imshow('extract.png',biometric)
    
#test()

import cv2
import numpy as np
import random

class Embedder:
    def __init__(self,passes,key,channels,depth,mask,logging=False):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        self.CHANNELS = channels
        self.DEPTH = depth
        self.MASK = mask
        self.logging = logging

    def embed(self,biometric,carrier):
        # Load the carrier image
        carrierImg = cv2.imread(carrier)

        # Load the biometric image
        biometricImg = cv2.imread(biometric)
        biometricImg = cv2.cvtColor(biometricImg,cv2.COLOR_BGR2GRAY)
        biometricX = biometricImg.shape[0]
        biometricY = biometricImg.shape[1]

        # Seed the PRG
        random.seed(self.KEY)

        # Debug
        self.table = []

        rotateIJ = lambda i,j,orientation: \
            (i,j) if orientation == 0 \
            else rotateIJ(j,-i-1,orientation-1)
        
        def runPass(passNumber):
            # Select channel to hide data
            channel = passNumber % self.CHANNELS

            orientation = passNumber%4
            
            shape = [[carrierImg.shape[0],carrierImg.shape[1]],
                     [carrierImg.shape[1],carrierImg.shape[0]]]
            
            for i in range(biometricX):
                for j in range(biometricY):
                    x = random.randint(0,shape[passNumber%2][0]-1)
                    y = random.randint(0,shape[passNumber%2][1]-1)
                    
                    x,y = rotateIJ(x,y,orientation)
                    
                    # Get the n MSBs for the biometric and shift it
                    # to the second last LSB and onwards
                    dataToHide = (biometricImg[i,j] >> (8 - self.DEPTH)) << 1
                    
                    # Set the bits to 0 where the data is to be hidden
                    carrierImg[x,y,channel] &= self.MASK

                    # Set the bits of the image
                    carrierImg[x,y,channel] |= dataToHide
                    #carrierImg[x,y,channel] = 255 # Debug

                    # Debug
                    if i == 64 and passNumber == 2 and self.logging:
                        row = [passNumber,i,j,x,y,dataToHide]
                        self.table.append(row)

        for i in range(self.NUMBER_OF_PASSES):
            runPass(i)

        # Debug
        if self.logging:
            with open('embed.txt','w') as f:
                f.write(str(self.table))

        return carrierImg

def test():
    KEY = 1234
    CHANNELS = 3
    NUMBER_OF_PASSES = 8
    DEPTH = 2
    MASK = 249

    carrier = '../Carrier.png'
    biometric = '../FingerPrint.png'
    output = './out'+str(NUMBER_OF_PASSES)+'.png'

    embedder = Embedder(NUMBER_OF_PASSES,KEY,CHANNELS,DEPTH,MASK,False)
    result = embedder.embed(biometric,carrier)
    cv2.imwrite(output,result)    
    
#test()


import cv2
import numpy as np
import random

class Embedder:
    def __init__(self,passes,key,channels,depth,mask):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        self.CHANNELS = channels
        self.depth = depth
        self.mask = mask

    def embed(self,biometric,carrier,output):
        # Load the carrier image
        carrierImg = cv2.imread(carrier)

        # Load the biometric image
        biometricImg = cv2.imread(biometric)
        biometricImg = cv2.cvtColor(biometricImg,cv2.COLOR_BGR2GRAY)
        biometricX = biometricImg.shape[0]
        biometricY = biometricImg.shape[1]

        # Seed the PRG
        random.seed(KEY)

        def runPass(carrierImg,passNumber):
            # Select channel to hide data
            channel = passNumber % CHANNELS

            # Rotate the carrier image by 90 degrees CCW
            carrierImg = np.rot90(carrierImg,1)
            carrierX = carrierImg.shape[0]
            carrierY = carrierImg.shape[1]
            
            for i in range(biometricX):
                for j in range(biometricY):
                    x = random.randint(0,carrierX-1)
                    y = random.randint(0,carrierY-1)
                    
                    # Get the n MSBs for the biometric and shift it
                    # to the second last LSB and onwards
                    dataToHide = (biometricImg[i,j] >> (8 - self.depth)) << 1
                    
                    # Set the bits to 0 where the data is to be hidden
                    carrierImg[x,y,channel] &= self.mask

                    # Set the bits of the image
                    carrierImg[x,y,channel] |= dataToHide

        for i in range(NUMBER_OF_PASSES):
            runPass(carrierImg,i)

        # Reorient the image
        carrierImg = np.rot90(carrierImg,NUMBER_OF_PASSES%4)

        #cv2.imshow(output,carrierImg)
        cv2.imwrite(output,carrierImg)

def test():
    KEY = 1234
    CHANNELS = 3
    NUMBER_OF_PASSES = 8
    DEPTH = 2
    MASK = 249

    carrier = '../Carrier.png'
    biometric = '../FingerPrint.png'
    output = './out'+str(NUMBER_OF_PASSES)+'.png'

    embedder = Embedder(NUMBER_OF_PASSES,KEY,CHANNELS,DEPTH,MASK)

    embedder.embed(biometric,carrier,output)
    
test()


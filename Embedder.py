from PIL import Image
import random

class Embedder:
    def __init__(self,passes,key,channels,shift):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        random.seed(self.KEY)
        self.CHANNELS = channels
        self.shift = shift
        self.bits = (1<<self.shift)-1

    def embed(self,biometric,carrier,output):
        # Load the carrier and biometric images
        carrierFile = Image.open(carrier)
        biometricFile = Image.open(biometric)
        carrierPix = carrierFile.load()
        biometricPix = biometricFile.load()

        # Hide data in LSB of a channel (RGBA)
        def hideData(rgba,val,channel):
            rgba = list(rgba)
            rgba[channel] = ((rgba[channel]>>self.bits)<<self.bits) + val
            return tuple(rgba)

        # One iteration of the stenography
        def runPass(channel):
            for i in range(biometricFile.size[0]):
                for j in range(biometricFile.size[1]):
                    x = random.randint(0,carrierFile.size[0]-1)
                    y = random.randint(0,carrierFile.size[1]-1)
                    carrierPix[x,y] = hideData(carrierPix[x,y],
                                               biometricPix[i,j][0]>>(8-(self.shift)),
                                               channel)   


        # Run multiple passes
        for i in range(self.NUMBER_OF_PASSES):
            runPass(i % self.CHANNELS)

        # Save output
        carrierFile.save(output)
        carrierFile.show()

        # Close all open files
        carrierFile.close()
        biometricFile.close()

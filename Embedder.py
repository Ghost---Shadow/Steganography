from PIL import Image
import random

# Level of redundancy
NUMBER_OF_PASSES = 10

# Change private key as required
PRIVATE_KEY = 1234
random.seed(PRIVATE_KEY)

# Load the carrier and biometric images
carrierFile = Image.open("./Carrier.png")
biometricFile = Image.open("./FingerPrint.png")
carrierPix = carrierFile.load()
bufferPix = carrierFile.copy().load()
biometricPix = biometricFile.load()

# Hide data in LSB of a channel (RGBA)
def hideData(rgba,val,channel):
    rgba = list(rgba)
    rgba[channel] = ((rgba[channel]>>1)<<1) + val
    return tuple(rgba)

# One iteration of the stenography
def runPass(channel):
    for i in range(biometricFile.size[0]):
        for j in range(biometricFile.size[1]):
            x = random.randint(0,carrierFile.size[0]-1)
            y = random.randint(0,carrierFile.size[1]-1)
            carrierPix[x,y] = hideData(carrierPix[x,y],
                                       biometricPix[i,j][0]//255,
                                       channel)   


# Run multiple passes
for i in range(NUMBER_OF_PASSES):
    runPass(i%4)

# Save output
carrierFile.save("output.png")
carrierFile.show()

# Close all open files
carrierFile.close()
biometricFile.close()



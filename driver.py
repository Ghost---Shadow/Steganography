from embedder import Embedder
from extractor import Extractor

import random
import time

current_milli_time = lambda: int(round(time.time() * 1000))

# File names
CARRIER = "./Carrier.png"
BIOMETRIC = "./FingerPrint.png"
EMBEDDED = "./Output.png"
EXTRACTED = "./Tests/Ex"

# Number of channels (RGBA)
CHANNELS = 4

# Level of redundancy
NUMBER_OF_PASSES = 4

# Change key as required
KEY = 1234

# Level of clarity
shift = 2

# Dimension of biometric
N = 128

print("Embedding image")
# Embed the biometric onto the carrier
embedObject = Embedder(NUMBER_OF_PASSES,KEY,CHANNELS,shift)
embedObject.embed(BIOMETRIC,CARRIER,EMBEDDED)
print("Done")

# Extract the biometric from the file EMBEDDED
extractObject = Extractor(NUMBER_OF_PASSES,KEY,CHANNELS,shift,N)
#extractObject.extract(EMBEDDED,EXTRACTED)

# Testing
NUMBER_OF_TESTS = 10
CARRIER_X = 620
CARRIER_Y = 387
for i in range(NUMBER_OF_TESTS):
    random.seed(current_milli_time())
    # Randomly generate cropping region
    x1,x2 = random.randint(0,CARRIER_X),random.randint(0,CARRIER_X)
    y1,y2 = random.randint(0,CARRIER_Y),random.randint(0,CARRIER_Y)
    crop = (min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))

    # Calculate ratio of cropped image to original image
    ratio = (crop[2]-crop[0])*(crop[3]-crop[1])/CARRIER_Y/CARRIER_X
    ratio = float("{0:.4f}".format(ratio))

    # Generate filename and write file
    fileName = EXTRACTED+str(NUMBER_OF_PASSES)+"_"+str(i)+"_"+str(ratio)+".png"
    print(fileName + "\t" + str(crop))
    extractObject.extract(EMBEDDED,crop,fileName)
print("Done")



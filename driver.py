#!/usr/bin/env python3

import cv2

from mypackage.embedder import Embedder
from mypackage.extractor import Extractor
from mypackage.guidelines import GuideLines

import random
import time

current_milli_time = lambda: int(round(time.time() * 1000))

# File names
CARRIER = "./Carrier.png"
BIOMETRIC = "./FingerPrint.png"
EMBEDDED = "./Output.png"
EXTRACTED = "./Tests_PNG/Test"

# Number of channels (RGBA)
CHANNELS = 3 

# Level of redundancy
NUMBER_OF_PASSES = 32

# Change key as required
KEY = 1234

# Level of clarity
DEPTH = 2

# Brightness increase, 2^5 = 32 times
SHIFT = 5

# The data is going to be embedded in ~MASK
MASK = 249

# Where the guidelines are stored
GUIDE_MASK = 1

# Number of tests
NUMBER_OF_TESTS = 20

# Assuming square image
biometric = cv2.imread(BIOMETRIC)
BIOMETRIC_SIZE = biometric.shape[0]

# Read the carrier file
carrier = cv2.imread(CARRIER)

guideLines = GuideLines()

print('Generating guide lines')
carrier = guideLines.washBitDepth(carrier,~GUIDE_MASK)
carrier = guideLines.generateGuideLines(carrier,GUIDE_MASK)

print('Embedding image')
embedder = Embedder(NUMBER_OF_PASSES,KEY,CHANNELS,DEPTH,MASK)
embedded = embedder.embed(biometric,carrier)
cv2.imwrite(EMBEDDED,embedded)
print('Done')

extractor = Extractor(NUMBER_OF_PASSES,KEY,~MASK,SHIFT)

embedded = cv2.imread(EMBEDDED)

CARRIER_X = embedded.shape[0]
CARRIER_Y = embedded.shape[1]

for i in range(NUMBER_OF_TESTS):
    print('Test '+str(i))
    
    random.seed(current_milli_time())
    x1 = int(CARRIER_X/2) - random.randint(0,int(CARRIER_X/3))
    x2 = int(CARRIER_X/2) + random.randint(0,int(CARRIER_X/3))

    y1 = int(CARRIER_Y/2) - random.randint(0,int(CARRIER_Y/3))
    y2 = int(CARRIER_Y/2) + random.randint(0,int(CARRIER_Y/3))
    crop = (x1,y1,x2,y2)
    print(crop)
    
    cropped = embedded[crop[0]:crop[2],crop[1]:crop[3]]
    cv2.imwrite(EXTRACTED+str(i)+'.png',cropped)
    
    margins = guideLines.getMargins(cropped,GUIDE_MASK)
    corners = guideLines.marginsToCorners(margins)
    actualSize = guideLines.getActualSize(cropped,margins)
    extract = extractor.extract(cropped,corners,actualSize,BIOMETRIC_SIZE)

    cv2.imwrite(EXTRACTED+str(i)+'_bio.png',extract)









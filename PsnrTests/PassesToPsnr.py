import sys
sys.path.append('../steganography')
from embedder import Embedder
from extractor import Extractor
from guidelines import GuideLines
import cv2
import matplotlib.pyplot as plt
import numpy as np

MAX_PASSES = 32
KEY = 1234
DEPTH = 2
CHANNELS = 3
MASK = 249
SHIFT = 5
GUIDE_MASK = 1

CARRIER = "../Carrier.png"
BIOMETRIC = "../FingerPrint.png"
EXPECTED = "./Expected.png"

biometric = cv2.imread(BIOMETRIC)
carrier = cv2.imread(CARRIER)
expected = cv2.cvtColor(cv2.imread(EXPECTED),cv2.COLOR_BGR2GRAY)

BIOMETRIC_SIZE = biometric.shape[0]
CARRIER_SIZE = carrier.shape

gl = GuideLines()

carrier = gl.washBitDepth(carrier,~GUIDE_MASK)
carrier = gl.generateGuideLines(carrier,GUIDE_MASK)

x1 = int(CARRIER_SIZE[0]/2) - int(CARRIER_SIZE[0]/4)
x2 = int(CARRIER_SIZE[0]/2) + int(CARRIER_SIZE[0]/4)

y1 = int(CARRIER_SIZE[1]/2) - int(CARRIER_SIZE[1]/4)
y2 = int(CARRIER_SIZE[1]/2) + int(CARRIER_SIZE[1]/4)
crop = (x1,y1,x2,y2)

untouched = carrier[crop[0]:crop[2],crop[1]:crop[3]]

em_psnr = []
ex_psnr = []
for passes in range(MAX_PASSES):
    em = Embedder(passes,KEY,CHANNELS,DEPTH,MASK)
    ex = Extractor(passes,KEY,~MASK,SHIFT)
    
    embedded = em.embed(biometric,carrier)

    cropped = embedded[crop[0]:crop[2],crop[1]:crop[3]]
    margins = gl.getMargins(cropped,GUIDE_MASK)
    corners = gl.marginsToCorners(margins)
    actualSize = gl.getActualSize(cropped,margins)
    
    extracted = ex.extract(cropped,corners,actualSize,BIOMETRIC_SIZE)
    ex_psnr.append(cv2.PSNR(expected,extracted))
    em_psnr.append(cv2.PSNR(np.uint8(cropped),np.uint8(untouched)))
    print(passes,em_psnr[-1],ex_psnr[-1])

cv2.imwrite('./final.png',extracted)
plt.plot(em_psnr,'b')
plt.plot(ex_psnr,'r')
plt.show()

    

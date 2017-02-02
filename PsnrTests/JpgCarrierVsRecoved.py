import sys
sys.path.append('../steganography')
from embedder import Embedder
from extractor import Extractor
import cv2
import matplotlib.pyplot as plt

ITERATIONS = 30
PASSES = 32
KEY = 1234
DEPTH = 2
CHANNELS = 3
MASK = 249
SHIFT = 5

CARRIER = "../Carrier2.jpg"
BIOMETRIC = "../FingerPrint.png"
EXPECTED = "./Expected.png"

biometric = cv2.imread(BIOMETRIC)
carrier = cv2.imread(CARRIER)
expected = cv2.cvtColor(cv2.imread(EXPECTED),cv2.COLOR_BGR2GRAY)

BIOMETRIC_SIZE = biometric.shape[0]
actualSize = carrier.shape
corners = [[0,0],[0,0],[0,0],[0,0]]

embedded = carrier.copy()

em = Embedder(PASSES,KEY,CHANNELS,DEPTH,MASK)
ex = Extractor(PASSES,KEY,~MASK,SHIFT)

em_psnr = []
ex_psnr = []
for iteration in range(ITERATIONS):
    embedded = em.embed(biometric,embedded)
    filename = './CarrierVsRecoved/Iteration_'+str(iteration)+'.jpg'
    cv2.imwrite(filename,embedded)
    embedded = cv2.imread(filename)
    em_psnr.append(cv2.PSNR(carrier,embedded))
    
    extracted = ex.extract(embedded,corners,actualSize,BIOMETRIC_SIZE)
    ex_psnr.append(cv2.PSNR(expected,extracted))
    print(iteration,em_psnr[-1],ex_psnr[-1])

cv2.imwrite('./CarrierVsRecoved/final.png',extracted)
plt.plot(em_psnr,'b')
plt.plot(ex_psnr,'r')
plt.show()

    

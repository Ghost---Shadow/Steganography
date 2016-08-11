from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random

carrier = Image.open('./DctTest.jpg')
carrier = carrier.convert('YCbCr')
pix = carrier.load()

random.seed(1234)

randomMatrix = [[127 for j in range(carrier.size[1])] for i in range(carrier.size[0])]

x = [0 for _ in range(carrier.size[1] * carrier.size[0])]
y = [randomMatrix[int(i/carrier.size[0])][i%carrier.size[0]] for i in range(carrier.size[1] * carrier.size[0])]

for i in range(carrier.size[0]):
    for j in range(carrier.size[1]):
        ycbcr = list(pix[i,j])
        ycbcr = tuple([ycbcr[0],randomMatrix[i][j],127])
        pix[i,j] = ycbcr

carrier.save('./DctTestOutput.jpg')
carrier.close()

crossCheck = Image.open('./DctTestOutput.jpg')
crossCheck = crossCheck.convert('YCbCr')
pix = crossCheck.load()

for i in range(carrier.size[0]):
    for j in range(carrier.size[1]):
        x[carrier.size[0] * i + j] = pix[i,j][1]       

crossCheck.close()

X = np.vstack((x,y))
print(np.cov(X))

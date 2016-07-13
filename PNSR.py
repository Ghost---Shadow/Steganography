from PIL import Image
import math
import functools as ft
import operator

def calculatePNSR(originalImage,newImage,channels=3):
##    h1 = originalImage.histogram()
##    h2 = newImage.histogram()
##
##    rms = math.sqrt(ft.reduce(operator.add,
##        map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

    m = originalImage.size[0]
    n = originalImage.size[1]

    originalPix = originalImage.load()
    newPix = newImage.load()

    rms = 0.0

    #luma = [.299,.587,.114]
    luma = [.2126,.7152,.0722]
    
    for i in range(m):
        for j in range(n):
            if channels == 3:
                yOld = sum([luma[k] * originalPix[i,j][k] for k in range(3)])
                yNew = sum([luma[k] * newPix[i,j][k] for k in range(3)])
            else:
                yOld = originalPix[i,j]
                yNew = newPix[i,j][0]
            rms += (yOld - yNew) ** 2
            
    rms /= n * m
    
    psnr = 20 * math.log10(255.0/math.sqrt(rms))

    return psnr,rms


##originalImage = Image.open('./PSNR_TEST/PSNR-example-base.png')
##newImage = Image.open('./PSNR_TEST/200px-PSNR-example-comp-90.jpg')
##print(calculatePNSR(originalImage,newImage,3))

##originalImage = Image.open('./PSNR_TEST/Original.png')
##newImage = Image.open('./PSNR_TEST/New.png')
##print(calculatePNSR(originalImage,newImage,1))

originalImage = Image.open('./Carrier.png')
newImage = Image.open('./output.png')
print(calculatePNSR(originalImage,newImage,3))

##originalImage = Image.open('./Carrier.jpg')
##newImage = Image.open('./output.jpg')
##print(calculatePNSR(originalImage,newImage,3))


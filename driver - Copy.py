from PIL import Image
import random

class Embedder:
    def __init__(self,passes,key,channels,shift):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        self.CHANNELS = channels
        self.shift = shift
        self.bits = (1<<self.shift)-1
        self.offset = 0

    def embed(self,biometric,carrier,output):       
        # Load the carrier and biometric images
        carrierFile = Image.open(carrier)
        biometricFile = Image.open(biometric)
        carrierPix = carrierFile.load()
        biometricPix = biometricFile.load()
        assert carrierPix is not None
        assert biometricPix is not None

        # If file is .jpg go to YCbCr domain
        if carrier[-3:] == 'jpg':
            self.offset = 1
            self.CHANNELS = 2
            carrierFile = carrierFile.convert('YCbCr')

        # Seed the PRG
        random.seed(self.KEY)

        # Hide data in LSB of a channel (RGBA) or (YCbCr)
        def hideData(rgba,val,channel):
            assert channel < len(rgba), str(channel)
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
            runPass(self.offset+i % self.CHANNELS)

        # Save output
        carrierFile.save(output)
        #carrierFile.show()

        # Close all open files
        carrierFile.close()
        biometricFile.close()

class Extractor:
    def __init__(self,passes,key,channels,shift,N):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key        
        self.CHANNELS = channels
        self.shift = shift
        self.bits = (1<<self.shift)-1
        self.N = N
        self.BLANK_PIXEL = 1 << 8
        self.offset = 0

        # Save the votes
        self.votes = [[[] for i in range(self.N)] for j in range(self.N)]

    def extract(self,inputPath,crop,outputPath):
        # Load the image
        hiddenFile = Image.open(inputPath)
        hiddenPix = hiddenFile.load()
        extractedFile = Image.new("RGB",(self.N,self.N),"white")
        extractedPix = extractedFile.load()

        # If file is .jpg go to YCbCr domain
        if inputPath[-3:] == 'jpg':
            self.offset = 1
            self.CHANNELS = 2
            hiddenFile = hiddenFile.convert('YCbCr')

        # Seed the PRG
        random.seed(self.KEY)

        # Check if pixel is within bounds
        def withinBounds(x,y):
            return x >= crop[0] and y >= crop[1] and x < crop[2] and y < crop[3] 
        
        # Load data hidden in LSB of a channel (RGBA)
        def getData(x,y,channel):
            rgba = list(hiddenPix[x,y])
            val = (rgba[channel] & self.bits) << (8-self.shift)
            return val

        # One iteration of the stenography
        def runPass(channel):
            for i in range(self.N):
                for j in range(self.N):
                    x = random.randint(0,hiddenFile.size[0]-1)
                    y = random.randint(0,hiddenFile.size[1]-1)
                    #extractedPix[i,j] = getData(x,y,channel)
                    if withinBounds(x,y):
                        self.votes[i][j].append(getData(x,y,channel))      

        # Run multiple passes
        for i in range(self.NUMBER_OF_PASSES):
            runPass(i % self.CHANNELS)

        # Resolve a vote
        def majorityVote(a):
            if len(a) == 0:
                return self.BLANK_PIXEL
            return max(map(lambda val: (a.count(val), val), set(a)))[1]        
            #return Counter(v).most_common(1)[0][0]

        # Resolve all votes
        for i in range(self.N):
            for j in range(self.N):
                pixel = majorityVote(self.votes[i][j])
                extractedPix[i,j] = (pixel,)*(self.CHANNELS+self.offset)

        # Close files
        hiddenFile.close()
        extractedFile.save(outputPath)
        #extractedFile.show()
        extractedFile.close()

import random
import time

current_milli_time = lambda: int(round(time.time() * 1000))

# File names
CARRIER = "./Carrier.j2k"
BIOMETRIC = "./FingerPrint.png"
EMBEDDED = "./Output.j2k"
EXTRACTED = "./Tests_JPX/Ex"

# Number of channels (RGBA)
CHANNELS = 3 # does nothing if file is .jpg

# Level of redundancy
NUMBER_OF_PASSES = 8

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



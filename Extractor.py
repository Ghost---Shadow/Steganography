from PIL import Image
import random
#from collections import Counter

class Extractor:
    def __init__(self,passes,key,channels,shift,N):
        self.NUMBER_OF_PASSES = passes
        self.KEY = key
        random.seed(self.KEY)
        self.CHANNELS = channels
        self.shift = shift
        self.bits = (1<<self.shift)-1
        self.N = N

        # Save the votes
        self.votes = [[[] for i in range(self.N)] for j in range(self.N)]
            
    def extract(self,inputPath,outputPath):
        # Load the image
        hiddenFile = Image.open(inputPath)
        hiddenPix = hiddenFile.load()
        extractedFile = Image.new("RGB",(self.N,self.N),"white")
        extractedPix = extractedFile.load()

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
                    self.votes[i][j].append(getData(x,y,channel))      

        # Run multiple passes
        for i in range(self.NUMBER_OF_PASSES):
            runPass(i % self.CHANNELS)

        # Resolve a vote
        def majorityVote(a):
            #return Counter(v).most_common(1)[0][0]
            return max(map(lambda val: (a.count(val), val), set(a)))[1]

        # Resolve all votes
        for i in range(self.N):
            for j in range(self.N):
                pixel = majorityVote(self.votes[i][j])
                extractedPix[i,j] = (pixel,)*self.CHANNELS

        # Close files
        hiddenFile.close()
        extractedFile.save(outputPath)
        extractedFile.show()
        extractedFile.close()

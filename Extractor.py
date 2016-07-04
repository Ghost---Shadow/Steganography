from PIL import Image
import random
from collections import Counter

# Level of redundancy
NUMBER_OF_PASSES = 8

# Change key as required
KEY = 1234
random.seed(KEY)

# Level of clarity
shift = 2
bits = (1<<shift)-1

# Fingerprint dimension
N = 128

# Save the votes
votes = [[[] for i in range(N)] for j in range(N)]

# Load the image
hiddenFile = Image.open("./output.png")
hiddenPix = hiddenFile.load()
extractedFile = Image.new("RGB",(N,N),"white")
extractedPix = extractedFile.load()

# Load data hidden in LSB of a channel (RGBA)
def getData(x,y,channel):
    rgba = list(hiddenPix[x,y])
    val = (rgba[channel] & bits) << (8-shift)
    return val

# One iteration of the stenography
def runPass(channel):
    for i in range(N):
        for j in range(N):
            x = random.randint(0,hiddenFile.size[0]-1)
            y = random.randint(0,hiddenFile.size[1]-1)
            #extractedPix[i,j] = getData(x,y,channel)
            votes[i][j].append(getData(x,y,channel))      

# Run multiple passes
for i in range(NUMBER_OF_PASSES):
    runPass(i%4)

# Resolve a vote
def majorityVote(a):
    #return Counter(v).most_common(1)[0][0]
    return max(map(lambda val: (a.count(val), val), set(a)))[1]

# Resolve all votes
for i in range(N):
    for j in range(N):
        pixel = majorityVote(votes[i][j])
        extractedPix[i,j] = (pixel,)*3

# Close files
hiddenFile.close()
extractedFile.save("extract.png")
extractedFile.show()
extractedFile.close()

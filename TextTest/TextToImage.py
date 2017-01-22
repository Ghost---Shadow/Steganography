import numpy as np
import cv2
import os,re

# Break ASCII to binary, split it in chunks and then bit shift them to MSBs
def encode(text,depth):
    data = []
    for character in text:
        b = bin(ord(character))[2:]
        while len(b) < 8:
            b = '0' + b
        data.extend([int(b[i:i+depth],2)<<(8-depth) for i in range(0, len(b), depth)])
    return data

# Undo encode
def decode(data,depth):
    s = ""
    for i in range(0,len(data),4):
        b = 0
        for j in range(8//depth):
            b += data[i+j] >> (j * depth)
        s += chr(b)
    return s

# Repeat the data onto the entire image
def generateImage(canvas,data):
    counter = 0
    shape = canvas.shape
    dataLen = len(data)
    for x in range(shape[0]):
        for y in range(shape[1]):
            canvas[x,y] = data[counter]
            counter += 1
            counter %= dataLen
    return canvas

# Recover the data list from the extracted image
def getDataFromImage(img,msgLength,depth):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    dataLength = msgLength * (8//depth)
    votes = [[] for _ in range(dataLength)]
    shape = img.shape
    counter = 0
    for x in range(shape[0]):
        for y in range(shape[1]):
            votes[counter].append(img[x,y])
            counter += 1
            counter %= dataLength
    recovered = []
    for vote in votes:
        value = max(map(lambda val: (vote.count(val), val), set(vote)))[1]
        recovered.append(value)
    return recovered

def test():
    canvas = cv2.imread('./Blank.png')
    canvas = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    text = "The quick brown fox jumps over the lazy dog."
    DEPTH = 2
    data = encode(text,DEPTH)
    canvas = generateImage(canvas,data)
    cv2.imwrite('./canvas.png',canvas)

    for file in os.listdir('./Tests'):
        match = re.search('Test[0-9]+_bio*',file)
        if match:
            img = cv2.imread('./Tests/'+file)
            decodedData = getDataFromImage(img,len(text),DEPTH)
            decodedText = decode(decodedData,DEPTH)
            print(file,decodedText)

test()


















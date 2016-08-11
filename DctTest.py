from PIL import Image
from array import *

#testFile = Image.open('./DctTest.jpg')
#testFile = Image.open('./Carrier.jpg')                      
tables = testFile.quantization

#JpegImagePlugin.convert_dict_qtables(tables)

for i in tables:
    x = list(tables[i])
    average = sum(x)/len(x)

    #x = [int(average) for _ in x]
    x = [10 for _ in x]

    tables[i] = array('b',x)

testFile.save("./DctTestOutput.jpg",qtables=tables)
testFile.close()

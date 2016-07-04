from embedder import Embedder
from extractor import Extractor

# File names
CARRIER = "./Carrier.png"
BIOMETRIC = "./FingerPrint.png"
EMBEDDED = "./Output.png"
EXTRACTED = "./Tests/Extract"

# Number of channels (RGBA)
CHANNELS = 4

# Level of redundancy
NUMBER_OF_PASSES = 32

# Change key as required
KEY = 1234

# Level of clarity
shift = 2

# Dimension of biometric
N = 128

# Embed the biometric onto the carrier
embedObject = Embedder(NUMBER_OF_PASSES,KEY,CHANNELS,shift)
embedObject.embed(BIOMETRIC,CARRIER,EMBEDDED)

# Extract the biometric from the file EMBEDDED
extractObject = Extractor(NUMBER_OF_PASSES,KEY,CHANNELS,shift,N)
#extractObject.extract(EMBEDDED,EXTRACTED)

# Testing
crop = (0,0,310,190)
extractObject.extract(EMBEDDED,crop,EXTRACTED+"_UpperLeftQuad.png")

crop = (310,190,620,387)
extractObject.extract(EMBEDDED,crop,EXTRACTED+"_LowerRightQuad.png")

print("Done")



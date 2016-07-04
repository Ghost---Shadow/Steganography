from embedder import Embedder
from extractor import Extractor

# File names
CARRIER = "./Carrier.png"
BIOMETRIC = "./FingerPrint.png"
EMBEDDED = "./Output.png"
EXTRACTED = "./Extract.png"

# Number of channels (RGBA)
CHANNELS = 4

# Level of redundancy
NUMBER_OF_PASSES = 8

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
extractObject.extract(EMBEDDED,EXTRACTED)

print("Done")



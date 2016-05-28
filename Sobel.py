from PIL import Image
import math as m

# Load the image
im = Image.open("blur.jpg")

# Load all the pixels
pix = im.load()

# Create a copy of the pixels
buffer = im.copy().load()

# Kernels for sobel
kernelX = [[-1,0,1],
          [-1,0,1],
          [-1,0,1]]
		  
kernelY = [[-1,-1,-1],
           [0,0,0],
           [1,1,1]]

# Store edge length of the kernel
klen = len(kernelX[0])

for x in range(klen//2,im.size[0]-klen//2):
    for y in range(klen//2,im.size[1]-klen//2):
        rx,gx,bx,ry,gy,by = 0,0,0,0,0,0
        # Take weighted sum
        for i in range(klen):
            for j in range(klen):
                kx = kernelX[i][j]
                ky = kernelY[i][j]
                (r1,g1,b1) = buffer[x+(i-klen//2),y+(j-klen//2)]
                rx += r1 * kx
                gx += g1 * kx
                bx += b1 * kx
                ry += r1 * ky
                gy += g1 * ky
                by += b1 * ky
                r = m.sqrt(rx * rx + ry * ry)
                g = m.sqrt(gx * gx + gy * gy)
                b = m.sqrt(bx * bx + by * by)
        pix[x,y] = int(r),int(g),int(b)
        #pix[x,y] = rx,gx,bx

# Write back the file    
im.save("sobel.jpg")















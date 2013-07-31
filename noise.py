import random
import math
from PIL import Image

rangeValue = 8192 

perm = range(rangeValue)
random.seed(42)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / rangeValue),
		 math.sin(a * 2.0 * math.pi / rangeValue))
		 for a in range(rangeValue)]

def noise(x, y, per):
	def surflet(gridX, gridY):
		distX, distY = abs(x-gridX), abs(y-gridY)
		polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
		polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
		hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
		grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
		return polyX * polyY * grad
	intX, intY = int(x), int(y)
	return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
			surflet(intX+0, intY+1) + surflet(intX+1, intY+1))

def fBm(x, y, per, octs):
	val = 0
	for o in range(octs):
		val += 0.5**o * noise(x*2**o, y*2**o, per*2**o)
	return val

def createImage(s, i, o):
	#size, freq, octs, data = s, 1/32.0, 5, []
	size, freq, octs, data = s, 1/8.0, o, []
	for y in range(size):
		for x in range(size*2):
			if y*i < 128 and y*i > 100 and x*i < 256 and x*i > 200:
				data.append((255,255,255))
			else:
				data.append((int(fBm((x*i)*freq, (y*i)*freq, int(size*freq), octs*2)*255),0,0))
	im = Image.new("RGB", (size*2, size))
	im.putdata(data, 128, 128)
	im.save("image"+ str(i) + ".png")


createImage(128, 1, 5)
createImage(128, 2, 4)
createImage(128, 3, 3)
createImage(128, 4, 2)
createImage(128, 5, 1)

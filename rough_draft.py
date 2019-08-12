from PIL import Image
from statistics import mean

black = (0, 0, 0)
white = (255, 255, 255)
dithers = {0:[[black]*2]*2, 63:[[black, black],[black, white]], 127:[[black, white],[white, black]], 191:[[black, white],[white, white]], 255:[[white]*2]*2}

straight_options = [0, 63, 127, 191, 255]

image_PATH = "/Users/ethanbolton/Desktop/BW/testImage.png"

im = Image.open(image_PATH)
rawdata = list(im.getdata())

averages = []
for point in rawdata:
	averages.append(int(mean((point[0], point[1], point[2]))))

MIN = int(min(averages))
MAX = int(max(averages))
MID = int(mean([MIN, MAX]))

options = [MIN, int(mean([MIN, MID])), MID, int(mean([MID, MAX])), MAX]

greys = []
for avg in averages:
	distances = {}
	for seg in options:
		distances[abs(avg - seg)] = seg

	closest_fit = distances[min(distances)]
	selection = straight_options[options.index(closest_fit)]
	greys.append(selection)

# print(greys)
print("STARTING DITHERING")

ditheredOut = []
newOne = []
newTwo = []
for ind, val in enumerate(greys):
	if ind % im.size[0] == 0:
		ditheredOut += (newOne + newTwo)
		newOne = []
		newTwo = []
	newOne += (dithers[val][0])
	newTwo += (dithers[val][1])

print(ditheredOut)
print(f"len of new data: {len(ditheredOut)}")
print(f"pixels in image: {((im.size[0]*2) * (im.size[1]*2))}")

newRes = (im.size[0]*2, im.size[1]*2)
newIm = Image.new("RGB", newRes)
newIm.putdata(ditheredOut)
newIm.save("/Users/ethanbolton/Desktop/BW/GREY_OUT.png")


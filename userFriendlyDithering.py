from PIL import Image
from statistics import mean
from pathlib import Path
from tqdm import tqdm 

black = (0, 0, 0)
white = (255, 255, 255)
dithers = {0:[[black]*2]*2, 63:[[black, black],[black, white]], 127:[[black, white],[white, black]], 191:[[black, white],[white, white]], 255:[[white]*2]*2}

straight_options = [0, 63, 127, 191, 255]

image_PATH = input("\n\tDrag file here: ").strip()

im = Image.open(image_PATH)
rawdata = list(im.getdata())

averages = []
print("\nGetting Averages...")
for point in tqdm(rawdata):
	averages.append(int(mean((point[0], point[1], point[2]))))

MIN = int(min(averages))
MAX = int(max(averages))
MID = int(mean([MIN, MAX]))

options = [MIN, int(mean([MIN, MID])), MID, int(mean([MID, MAX])), MAX]

greys = []
print("\nMaking greyscale...")
for avg in tqdm(averages):
	distances = {}
	for seg in options:
		distances[abs(avg - seg)] = seg

	closest_fit = distances[min(distances)]
	selection = straight_options[options.index(closest_fit)]
	greys.append(selection)


ditheredOut = []
newOne = []
newTwo = []
print("\nMaking new Image...")
for ind, val in tqdm(enumerate(greys)):
	if ind % im.size[0] == 0:
		ditheredOut += (newOne + newTwo)
		newOne = []
		newTwo = []
	newOne += (dithers[val][0])
	newTwo += (dithers[val][1])

newRes = (im.size[0]*2, im.size[1]*2)
newIm = Image.new("RGB", newRes)
newIm.putdata(ditheredOut)

fileName = input("\n\tWhat do you want to name the output file?: ")
if fileName.endswith('.png'):
	pass
else:
	fileName += '.png'

newIm.save(str(Path.home()) + "/Downloads/" + fileName)

print("\nFile has been saved to ~/Downloads/\n")

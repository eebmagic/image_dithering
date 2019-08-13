from PIL import Image
from statistics import mean
from pathlib import Path
from tqdm import tqdm
import sys
import os

# Get input image from command start
image_PATH = None
for i in sys.argv[1:]:
	try:
		im = Image.open(i).convert("LA")
		image_PATH = i
	except OSError:
		pass

# Get output name from command start
if '-o' in sys.argv[1:]:
	fileName = sys.argv[sys.argv[1:].index('-o') + 2]
	if not fileName.endswith('.png'):
		fileName += '.png'
else:
	fileName = None

# Get input image if none given yet
if not image_PATH:
	image_PATH = input("\n\tDrag file here: ").strip()
	im = Image.open(image_PATH).convert("LA")

# Check for user size in
if "--match" in sys.argv:
	im = im.resize((int(im.size[0] / 2), int(im.size[1] / 2)))

# Convert image to raw RGB
rawdata = [x[0] for x in list(im.getdata())]

# Configurations for dithering patterns
# Based on outline in evample_images/scale_guide.png
black = 0
white = 1
dithers = {
	0: [[black] * 2] * 2,
	63: [[black, black], [black, white]],
	127: [[black, white], [white, black]],
	191: [[black, white], [white, white]],
	255: [[white] * 2] * 2
}

straight_options = list(dithers.keys())

MIN = int(min(rawdata))
MAX = int(max(rawdata))
MID = int(mean([MIN, MAX]))

intervals = [MIN, int(mean([MIN, MID])), MID, int(mean([MID, MAX])), MAX]
seg_distances = []
for i in range(len(intervals) - 1):
	seg_distances.append(intervals[i + 1] - intervals[i])
min_jump_distance = min(seg_distances)

greys = []
print("\nRounding grayscale values to pattern keys...")
for avg in tqdm(rawdata):
	distances = {}
	for seg in intervals:
		distances[abs(avg - seg)] = seg

	closest_fit = distances[min(distances)]
	selection = straight_options[intervals.index(closest_fit)]
	greys.append(selection)


ditheredOut = []
newOne = []
newTwo = []
print("\nMaking patterns into new image...")
for ind, val in tqdm(enumerate(greys)):
	# If at end of row then reset
	if ind % im.size[0] == 0:
		ditheredOut += (newOne + newTwo)
		newOne = []
		newTwo = []
	newOne += (dithers[val][0])
	newTwo += (dithers[val][1])

newRes = (im.size[0] * 2, im.size[1] * 2)
newIm = Image.new("1", newRes)
newIm.putdata(ditheredOut)

if not fileName:
	fileName = input("\n\tWhat do you want to name the output file?: ")
	if not fileName.endswith('.png'):
		fileName += '.png'
print(f"Filename: {fileName}")
savePath = os.getcwd() + '/' + fileName
newIm.save(savePath)
print(f"\nImage saved to: {savePath}")

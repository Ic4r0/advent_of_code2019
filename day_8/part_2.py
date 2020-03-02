"""--- Day 8: Space Image Format - Part Two ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Store image data from file to variable
    image_data = file.readline()

WIDTH = 25
HEIGHT = 6

# Maximum number of digits per layer
PIXEL_PER_LAYER = WIDTH * HEIGHT
# Number of layers
N_LAYERS = len(image_data) // PIXEL_PER_LAYER

output_image = ['2'] * PIXEL_PER_LAYER

# For each pixel, find the first layer where that pixel is black or white
for pixel in range(PIXEL_PER_LAYER):
    for layer in range(N_LAYERS):
        if image_data[pixel + layer * PIXEL_PER_LAYER] == '0' or image_data[pixel + layer * PIXEL_PER_LAYER] == '1':
            output_image[pixel] = image_data[pixel + layer * PIXEL_PER_LAYER]
            break

# Print message (both version for the ease of the reader)
output_image_0 = [digit.replace('1', ' ') for digit in output_image]
output_image_0 = ''.join(output_image_0)
for line in range(HEIGHT):
    print(output_image_0[line * WIDTH:line * WIDTH + WIDTH])

output_image_1 = [digit.replace('0', ' ') for digit in output_image]
output_image_1 = ''.join(output_image_1)
for line in range(HEIGHT):
    print(output_image_1[line * WIDTH:line * WIDTH + WIDTH])

"""--- Day 8: Space Image Format - Part One ---"""

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

# Support variables for output
min_rep_zero = 150
rep_ones = None
rep_twos = None

# For each layer...
for start_layer in range(0, len(image_data), PIXEL_PER_LAYER):
    # ... check if the count of 0s is lesser than in previous layers
    if image_data[start_layer:start_layer + PIXEL_PER_LAYER].count('0') < min_rep_zero:
        min_rep_zero = image_data[start_layer:start_layer + PIXEL_PER_LAYER].count('0')
        rep_ones = image_data[start_layer:start_layer + PIXEL_PER_LAYER].count('1')
        rep_twos = image_data[start_layer:start_layer + PIXEL_PER_LAYER].count('2')

if rep_ones and rep_twos:
    print(rep_ones * rep_twos)

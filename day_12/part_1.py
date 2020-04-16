"""--- Day 12: The N-Body Problem - Part One ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    coords = []
    for line in file:
        # int_code.append([int(elem) for elem in line.split(',')])
        # print(line.split())
        # https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters

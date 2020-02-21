"""--- Day 6: Universal Orbit Map - Part Two ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    list_of_orbits = file.read().splitlines()

# Create a list of tuples (A, B) where B orbits A
for idx in range(len(list_of_orbits)):
    first, second = list_of_orbits[idx].split(')')
    list_of_orbits[idx] = (first, second)

# print(list_of_orbits[:5],list_of_orbits[-5:])

previous_iter = []

# Find the Center of Mass
for father, _ in list_of_orbits:
    counter = 0
    for _, child in list_of_orbits:
        if father == child:
            counter += 1
            break
    if counter == 0:
        center_of_mass = father

you = ['YOU']
san = ['SAN']

# Path from YOU/SAN to COM
while center_of_mass not in you:
    last_elem_of_you = you[-1]
    for father, child in list_of_orbits:
        if child == last_elem_of_you:
            you.append(father)
            break
while center_of_mass not in san:
    last_elem_of_san = san[-1]
    for father, child in list_of_orbits:
        if child == last_elem_of_san:
            san.append(father)
            break

# Path from YOU to SAN
path_from_you_to_san = list(set(you)^set(san))

# Output
print(len(path_from_you_to_san) - 2)
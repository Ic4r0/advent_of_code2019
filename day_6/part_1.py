"""--- Day 6: Universal Orbit Map - Part One ---"""

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
        previous_iter.append(father)

supp_orbits = list_of_orbits.copy()

# Number to be multiplied by the number of children of the previous iteration
orbits_per_iter = 1
# Output
total_number_orbits = 0

while supp_orbits:
    supp_previous_iter = []
    # Find all the children of the previous objects
    for obj in previous_iter:
        supp_previous_iter.extend([item for item in supp_orbits if item[0] == obj])
    # Remove all the relations father-children of this iteration
    for item in supp_previous_iter:
        supp_orbits.remove(item)
    # Create a list of objects for the next iteration
    for idx in range(len(supp_previous_iter)):
        supp_previous_iter[idx] = supp_previous_iter[idx][1]
    total_number_orbits += orbits_per_iter * len(supp_previous_iter)
    previous_iter = supp_previous_iter.copy()
    orbits_per_iter += 1

print(total_number_orbits)

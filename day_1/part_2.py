"""--- Day 1: The Tyranny of the Rocket Equation - Part Two---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where each element of it is a mass value
    list_of_mass = [int(line) for line in file.readlines()]

# List where there will be stored the fuel requirements for each module separately
fuel_requirements = []

# Compute the required fuel for a specific mass
for mass in list_of_mass:
    fuel_needed = mass // 3 - 2
    supp = fuel_needed // 3 - 2
    # While the supp value is positive then the loop continues
    while supp > 0:
        fuel_needed += supp
        supp = supp // 3 - 2
    fuel_requirements.append(fuel_needed)

# Compute the required result
print(sum(fuel_requirements))

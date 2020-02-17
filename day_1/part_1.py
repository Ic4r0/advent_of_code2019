"""--- Day 1: The Tyranny of the Rocket Equation - Part One---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where each element of it is a mass value
    list_of_mass = [int(line) for line in file.readlines()]

# Compute the fuel needed for each module
fuel_needed = [mass // 3 - 2 for mass in list_of_mass]

# Compute the required result
print(sum(fuel_needed))

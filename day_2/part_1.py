"""--- Day 2: 1202 Program Alarm - Part One ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

# Replace specific values inside the input list
int_code[1] = 12
int_code[2] = 2

# Start program
index = 0
while int_code[index] != 99 and index < len(int_code):
    if int_code[index] == 1:
        int_code[int_code[index + 3]] = int_code[int_code[index + 1]] + int_code[int_code[index + 2]]
    elif int_code[index] == 2:
        int_code[int_code[index + 3]] = int_code[int_code[index + 1]] * int_code[int_code[index + 2]]
    index += 4

# Print the required result
print(int_code[0])

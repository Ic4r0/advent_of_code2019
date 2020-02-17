"""--- Day 3: Crossed Wires - Part One ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input as a tuple (direction, steps)
    wires_directions = []
    for line in file:
        wires_directions.append([(elem[0], int(elem[1:])) for elem in line.split(',')])

def go_up(actual_position: tuple,
          steps: int):
    x, y = actual_position
    new_y = list(range(y+1, y+steps+1))
    return [(x, step) for step in new_y]

def go_down(actual_position: tuple,
            steps: int):
    x, y = actual_position
    new_y = list(range(y-steps, y))
    new_y.reverse()
    return [(x, step) for step in new_y]

def go_right(actual_position: tuple,
             steps: int):
    x, y = actual_position
    new_x = list(range(x+1, x+steps+1))
    return [(step, y) for step in new_x]

def go_left(actual_position: tuple,
            steps: int):
    x, y = actual_position
    new_x = list(range(x-steps, x))
    new_x.reverse()
    return [(step, y) for step in new_x]

def go_on(actual_position: tuple,
          coords: tuple):
    direction, steps = coords
    if direction == 'U':
        return go_up(actual_position, steps)
    elif direction == 'D':
        return go_down(actual_position, steps)
    elif direction == 'R':
        return go_right(actual_position, steps)
    elif direction == 'L':
        return go_left(actual_position, steps)

# Directions for each wire
wire_dir_1, wire_dir_2 = wires_directions

# Path for each wire
wire_1 = [(0, 0)]
wire_2 = [(0, 0)]

# Build the path followed by each wire
for coords in wire_dir_1:
    wire_1.extend(go_on(wire_1[-1], coords))
for coords in wire_dir_2:
    wire_2.extend(go_on(wire_2[-1], coords))

# Remove origin coordinates
wire_1 = wire_1[1:]
wire_2 = wire_2[1:]

# Find each different cross
crosses = list(set(wire_1).intersection(wire_2))

# Check the nearest cross to the origin
min_distance = 10**6
for cross in crosses:
    x_axis, y_axis = cross
    if min_distance > abs(x_axis) + abs(y_axis):
        min_distance = abs(x_axis) + abs(y_axis)

# Print the required result
print(min_distance)

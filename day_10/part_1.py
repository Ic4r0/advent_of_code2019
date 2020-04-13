"""--- Day 10: Monitoring Station - Part One ---"""

import os
import math

# Return all '#' positions
def find_coords(asteroid_list: list) -> list:
    row = 0
    asteroid_coords = []
    for line in asteroid_list:
        col = 0
        while True:
            try:
                # Search for item in list from indexPos to the end of list
                col = line.index('#', col)
                # Add the index position in list
                asteroid_coords.append((row, col))
                col += 1
            except ValueError as e:
                break
        row += 1
    return asteroid_coords

# Find number of reachable stations
def find_reachable_stations(asteroid_list: list,
                            couple: list,
                            max_rows: int,
                            max_cols: int) -> list:
    row, col = couple
    asteroid_list_copy = asteroid_list[:]
    asteroid_list_copy.remove(couple)

    # Find all the unreachable asteroids
    to_remove = []
    for elem_row, elem_col in asteroid_list_copy:
        row_dist = row - elem_row
        col_dist = col - elem_col
        row_col_gcd = math.gcd(row_dist, col_dist)
        row_dist /= row_col_gcd
        col_dist /= row_col_gcd
        next_row = elem_row - row_dist
        next_col = elem_col - col_dist
        while -1 < next_row < max_rows and -1 < next_col < max_cols:
            if (next_row, next_col) in asteroid_list_copy:
                if (next_row, next_col) not in to_remove:
                    to_remove.append((next_row, next_col))
            next_row -= row_dist
            next_col -= col_dist
    for elem in to_remove:
        asteroid_list_copy.remove(elem)

    return len(asteroid_list_copy)

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    input_list = []
    for line in file:
        input_list.append(list(line[:-1]))

MAX_ROWS = len(input_list)
MAX_COLS = len(input_list[0])

asteroids = find_coords(input_list)

number_of_reachable_asteroids = []
for elem in asteroids:
    number_of_reachable_asteroids.append(
        find_reachable_stations(asteroids, elem, MAX_ROWS, MAX_COLS)
    )

for elem in range(len(number_of_reachable_asteroids)):
    print(asteroids[elem], ' - ', number_of_reachable_asteroids[elem])

print('\nThe max value is ', max(number_of_reachable_asteroids), ' for ',
        asteroids[number_of_reachable_asteroids.index(max(
            number_of_reachable_asteroids))])

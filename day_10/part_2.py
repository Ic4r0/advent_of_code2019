"""--- Day 10: Monitoring Station - Part Two ---"""

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
            except ValueError:
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

    return asteroid_list_copy

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

# Giant laser location
LASER_ROW = 20
LASER_COL = 20

asteroids = find_coords(input_list)

destroyed_asteroids = []
reachable_asteroids = []
while len(destroyed_asteroids) < 200:
    reachable_asteroids = find_reachable_stations(
                                asteroid_list=asteroids,
                                couple=(LASER_ROW, LASER_COL),
                                max_rows=MAX_ROWS,
                                max_cols=MAX_COLS)

    # First quarter clockwise
    first_quarter = [elem for elem in reachable_asteroids
                        if elem[1] >= LASER_COL and elem[0] < LASER_ROW]
    first_quarter_tan = [(math.atan2(LASER_ROW-elem[0], elem[1]-LASER_COL),
                          elem) for elem in first_quarter]
    first_quarter_tan.sort(reverse=True)

    # Second quarter clockwise
    second_quarter = [elem for elem in reachable_asteroids
                        if elem[1] > LASER_COL and elem[0] >= LASER_ROW]
    second_quarter_tan = [(math.atan2(LASER_ROW-elem[0], elem[1]-LASER_COL),
                          elem) for elem in second_quarter]
    second_quarter_tan.sort(reverse=True)

    # Third quarter clockwise
    third_quarter = [elem for elem in reachable_asteroids
                        if elem[1] <= LASER_COL and elem[0] > LASER_ROW]
    third_quarter_tan = [(math.atan2(LASER_ROW-elem[0], elem[1]-LASER_COL),
                          elem) for elem in third_quarter]
    third_quarter_tan.sort(reverse=True)

    # Fourth quarter clockwise
    fourth_quarter = [elem for elem in reachable_asteroids
                        if elem[1] < LASER_COL and elem[0] <= LASER_ROW]
    fourth_quarter_tan = [(math.atan2(LASER_ROW-elem[0], elem[1]-LASER_COL),
                          elem) for elem in fourth_quarter]
    fourth_quarter_tan.sort(reverse=True)

    # Fill destroyed_asteroids list and remove elements from asteroids
    while len(first_quarter_tan) > 0:
        _, coords = first_quarter_tan.pop(0)
        destroyed_asteroids.append(coords)
        asteroids.remove(coords)
    while len(second_quarter_tan) > 0:
        _, coords = second_quarter_tan.pop(0)
        destroyed_asteroids.append(coords)
        asteroids.remove(coords)
    while len(third_quarter_tan) > 0:
        _, coords = third_quarter_tan.pop(0)
        destroyed_asteroids.append(coords)
        asteroids.remove(coords)
    while len(fourth_quarter_tan) > 0:
        _, coords = fourth_quarter_tan.pop(0)
        destroyed_asteroids.append(coords)
        asteroids.remove(coords)

result_asteroid = destroyed_asteroids[199]
row_res, col_res = result_asteroid
result_output = col_res * 100 + row_res
print('The 200th destroyed asteroid was the one at ', result_asteroid)
print('The result needed for the exercise is ', result_output )
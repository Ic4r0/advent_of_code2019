"""--- Day 10: Monitoring Station - Part One ---"""

import os

MAX_ROWS = 34
MAX_COLS = 34

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
def find_reachable_stations(asteroid_list:list,
                            couple: list) -> list:
    row, col = couple
    asteroid_list_copy = asteroid_list[:]
    asteroid_list_copy.remove(couple)
    asteroid_list_reachable = []

    # Remove asteroids not reachable in the same row/column from the selected
    # asteroid
    same_row_left = []
    same_row_right = []
    same_col_up = []
    same_col_down = []
    for elem in asteroid_list_copy:
        elem_row, elem_col = elem
        if elem_row == row and elem_col < col:
            same_row_left.append(elem)
            asteroid_list_copy.remove(elem)
        elif elem_row == row and elem_col > col:
            same_row_right.append(elem)
            asteroid_list_copy.remove(elem)
        elif elem_col == col and elem_row < row:
            same_col_up.append(elem)
            asteroid_list_copy.remove(elem)
        elif elem_col == col and elem_row > row:
            same_col_down.append(elem)
            asteroid_list_copy.remove(elem)
    while len(same_row_left) > 1:
        same_row_left.pop(0)
    asteroid_list_reachable.extend(same_row_left)
    while len(same_row_right) > 1:
        same_row_right.pop()
    asteroid_list_reachable.extend(same_row_right)
    while len(same_col_up) > 1:
        same_col_up.pop(0)
    asteroid_list_reachable.extend(same_col_up)
    while len(same_col_down) > 1:
        same_col_down.pop()
    asteroid_list_reachable.extend(same_col_down)

    # Remove asteroids not reachable in a 45 degree direction from the selected
    # asteroid
    same_diagonal_left_up = []
    supp_row = row - 1
    supp_col = col - 1
    while supp_row > -1 and supp_col > -1:
        if (supp_row, supp_col) in asteroid_list_copy:
            same_diagonal_left_up.append((supp_row, supp_col))
            asteroid_list_copy.remove((supp_row, supp_col))
        supp_row -= 1
        supp_col -= 1
    while len(same_diagonal_left_up) > 1:
        same_diagonal_left_up.pop()
    asteroid_list_reachable.extend(same_diagonal_left_up)

    same_diagonal_left_down = []
    supp_row = row + 1
    supp_col = col - 1
    while supp_row < MAX_ROWS and supp_col > -1:
        if (supp_row, supp_col) in asteroid_list_copy:
            same_diagonal_left_down.append((supp_row, supp_col))
            asteroid_list_copy.remove((supp_row, supp_col))
        supp_row += 1
        supp_col -= 1
    while len(same_diagonal_left_down) > 1:
        same_diagonal_left_down.pop()
    asteroid_list_reachable.extend(same_diagonal_left_down)

    same_diagonal_right_up = []
    supp_row = row - 1
    supp_col = col + 1
    while supp_row > -1 and supp_col < MAX_COLS:
        if (supp_row, supp_col) in asteroid_list_copy:
            same_diagonal_right_up.append((supp_row, supp_col))
            asteroid_list_copy.remove((supp_row, supp_col))
        supp_row -= 1
        supp_col += 1
    while len(same_diagonal_right_up) > 1:
        same_diagonal_right_up.pop()
    asteroid_list_reachable.extend(same_diagonal_right_up)

    same_diagonal_right_down = []
    supp_row = row + 1
    supp_col = col + 1
    while supp_row < MAX_ROWS and supp_col < MAX_COLS:
        if (supp_row, supp_col) in asteroid_list_copy:
            same_diagonal_right_down.append((supp_row, supp_col))
            asteroid_list_copy.remove((supp_row, supp_col))
        supp_row += 1
        supp_col += 1
    while len(same_diagonal_right_down) > 1:
        same_diagonal_right_down.pop()
    asteroid_list_reachable.extend(same_diagonal_right_down)

    # Remove all the other unreachable asteroids
    for elem_row, elem_col in asteroid_list_copy:
        row_dist = row - elem_row
        col_dist = col - elem_col
        next_row = elem_row - row_dist
        next_col = elem_col - col_dist
        while -1 < next_row < MAX_ROWS and -1 < next_col < MAX_COLS:
            if (next_row, next_col) in asteroid_list_copy:
                asteroid_list_copy.remove((next_row, next_col))
            next_row -= row_dist
            next_col -= col_dist
    asteroid_list_reachable.extend(asteroid_list_copy)

    return len(asteroid_list_reachable)

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    input_list = []
    for line in file:
        input_list.append(list(line))

asteroid_reachable = find_coords(input_list)

number_of_reachable_asteroids = []
for elem in asteroid_reachable:
    number_of_reachable_asteroids.append(
        find_reachable_stations(asteroid_reachable, elem)
    )
print(max(number_of_reachable_asteroids))

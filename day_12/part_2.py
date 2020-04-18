"""--- Day 12: The N-Body Problem - Part Two ---"""

import os
import re
from copy import deepcopy

class MoonMotion:

    def __init__(self,
                 starting_position: list,
                 starting_velocity: list = [[0] * 3 for _ in range(4)],
                 n_coords: int = 3,
                 n_moons: int = 4):
        self.starting_position = starting_position
        self.starting_velocity = starting_velocity
        self.n_coords = n_coords
        self.n_moons = n_moons
    
    def moon_shift(self,
                   same_dimension: list,
                   selected_moon: int):
        counter = 0
        for moon_coord in same_dimension:
            if moon_coord > same_dimension[selected_moon]:
                counter += 1
            elif moon_coord < same_dimension[selected_moon]:
                counter -= 1
        return counter

    def compute_repetitions(self):
        steps_rep_index = []
        for coord in range(len(self.starting_position[0])):

            start_pos = [elem[coord] for elem in self.starting_position]
            current_pos = deepcopy(start_pos)
            start_vel = [elem[coord] for elem in self.starting_velocity]
            current_vel = deepcopy(start_vel)

            n_steps = 0
            while(True):
                n_steps += 1

                new_pos = [0] * self.n_moons
                new_vel = [0] * self.n_moons

                for moon in range(self.n_moons):
                    new_pos[moon] = current_pos[moon] + \
                            self.moon_shift(current_pos, moon) + \
                            current_vel[moon]
                    new_vel[moon] = new_pos[moon] - current_pos[moon]
                
                current_pos = new_pos
                current_vel = new_vel

                if current_pos == start_pos:
                    if current_vel == start_vel:
                        print('- ', n_steps, ' steps')
                        print('Current position: ', current_pos)
                        print('Current velocity: ', current_vel)
                        print('-------------------------------------')
                        steps_rep_index.append(n_steps)
                        break
                
                if (n_steps) % 500 == 0:
                    print('- ', n_steps, ' steps')
                    print('Current position: ', current_pos)
                    print('Current velocity: ', current_vel)
                    print('-------------------------------------')

        print('Steps to reach repetitions:')
        print('For coord x: ', steps_rep_index[0])
        print('For coord y: ', steps_rep_index[1])
        print('For coord z: ', steps_rep_index[2])
        output_lcm = 1
        for coord in steps_rep_index:
            output_lcm = self.find_lcm(output_lcm, coord)
        print(output_lcm)
    
    def find_lcm(self, num1, num2):
        num = max([num1, num2])
        den = min([num1, num2])
            
        rem = num % den

        while rem != 0:
            num = den
            den = rem
            rem = num % den

        return int(int(num1 * num2)/int(den))   # den is the gcd


COORDS_DIMENSIONS = 3
N_MOONS = 4
COORDS = [[0] * COORDS_DIMENSIONS for _ in range(N_MOONS)]

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    moon = 0
    input_pos = COORDS.copy()
    for line in file:
        match = re.match(r"^.*\=(.*),.*\=(.*),.*\=(.*)\>.*$", line)
        for coord in range(COORDS_DIMENSIONS):
            input_pos[moon][coord] = int(match.group(coord+1))
        moon += 1

part_1 = MoonMotion(input_pos)
part_1.compute_repetitions()

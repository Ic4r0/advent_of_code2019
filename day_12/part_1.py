"""--- Day 12: The N-Body Problem - Part One ---"""

import os
import re

class MoonMotion:

    def __init__(self,
                 starting_position: list,
                 starting_velocity: list = [[0] * 3 for _ in range(4)],
                 n_coords: int = 3,
                 n_moons: int = 4):
        self.current_pos = starting_position
        self.current_vel = starting_velocity
        self.n_coords = n_coords
        self.n_moons = n_moons
        self.pot_energy = [sum(moon_pos) for moon_pos in self.current_pos]
        self.kin_energy = [sum(moon_vel) for moon_vel in self.current_vel]
    
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

    def compute_pos_and_vel(self, n_steps: int):
        for i in range(n_steps):
            new_pos = [[0] * self.n_coords for _ in range(self.n_moons)]
            new_vel = [[0] * self.n_coords for _ in range(self.n_moons)]

            for moon in range(self.n_moons):
                for coord in range(self.n_coords):
                    new_pos[moon][coord] = self.current_pos[moon][coord] + \
                            self.moon_shift([elem[coord] for elem in 
                                                self.current_pos], moon) + \
                            self.current_vel[moon][coord]
                    new_vel[moon][coord] = new_pos[moon][coord] - \
                                            self.current_pos[moon][coord]
            
            self.current_pos = new_pos
            self.current_vel = new_vel
            self.pot_energy = [sum(abs(elem) for elem in moon_pos) for moon_pos
                                    in self.current_pos]
            self.kin_energy = [sum(abs(elem) for elem in moon_vel) for moon_vel
                                    in self.current_vel]

            if (i+1) % 25 == 0:
                print('- ', i+1, ' steps')
                print('Current position: ', self.current_pos)
                print('Current velocity: ', self.current_vel)
                print('-------------------------------------')
    
    def total_energy(self):
        total_energy = 0
        for single_moon in range(len(self.pot_energy)):
            total_energy += self.pot_energy[single_moon] * \
                self.kin_energy[single_moon]
        return total_energy


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
part_1.compute_pos_and_vel(1000)
print(part_1.total_energy())

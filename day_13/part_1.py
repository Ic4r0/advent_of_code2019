"""--- Day 13: Care Package - Part One ---"""

import os
from copy import deepcopy

class IntCode:
    index = 0
    relative_base = 0
    output_list = []
    nn_end = False

    def __init__(self,
                 intcode_list: list,
                 input_list: list = [],
                 instance_id: int = 0):
        self.intcode_list = deepcopy(intcode_list)
        self.input_list = deepcopy(input_list)
        self.instance_id = instance_id

    def manage_opcode(self):
        opcode = str(self.intcode_list[self.index]).zfill(5)
        returned_opcode = opcode[-2:]
        parameters = []
        for i in range(3):
            parameters.append(self.parameter_mode(opcode, i))
        return returned_opcode, parameters

    def parameter_mode(self,
                       opcode: str,
                       parameter_id: int):
        output_par = None
        if int(opcode[2-parameter_id]) == 0:
            output_par = self.intcode_list[self.index + parameter_id + 1]
        elif int(opcode[2-parameter_id]) == 1:
            output_par = self.index + parameter_id + 1
        elif int(opcode[2-parameter_id]) == 2:
            output_par = self.intcode_list[self.index + parameter_id + 1] + \
                            self.relative_base
        else:
            print('Error in parameter_mode')
        return output_par

    def expand_intcode_list(self, list_to_check: int):
        index_out_of_bound = max(list_to_check)
        self.intcode_list.extend([0] * (index_out_of_bound -
                                        len(self.intcode_list) + 1))

    def compute_int_code(self):
        while(True):
            opcode, parameters = self.manage_opcode()
            if opcode == '01':      # add opcode
                try:
                    self.intcode_list[parameters[2]] = \
                        self.intcode_list[parameters[0]] + \
                        self.intcode_list[parameters[1]]
                except:
                    self.expand_intcode_list(parameters)
                    self.intcode_list[parameters[2]] = \
                        self.intcode_list[parameters[0]] + \
                        self.intcode_list[parameters[1]]
                self.index += 4
            elif opcode == '02':    # multiply opcode
                try:
                    self.intcode_list[parameters[2]] = \
                        self.intcode_list[parameters[0]] * \
                        self.intcode_list[parameters[1]]
                except:
                    self.expand_intcode_list(parameters)
                    self.intcode_list[parameters[2]] = \
                        self.intcode_list[parameters[0]] * \
                        self.intcode_list[parameters[1]]
                self.index += 4
            elif opcode == '03':    # input opcode
                if len(self.input_list) > 0:
                    print("Using given input")
                    try:
                        self.intcode_list[parameters[0]] = self.input_list[0]
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[0]] = self.input_list[0]
                    self.input_list.pop(0)
                    self.index += 2
                else:
                    print("Waiting for an input")
                    break
            elif opcode == '04':    # output opcode
                try:
                    self.output_list.append(self.intcode_list[parameters[0]])
                except:
                    self.expand_intcode_list(parameters)
                    self.output_list.append(self.intcode_list[parameters[0]])
                self.index += 2
            elif opcode == '05':    # jump-if-true opcode
                if self.intcode_list[parameters[0]] != 0:
                    self.index = self.intcode_list[parameters[1]]
                else:
                    self.index += 3
            elif opcode == '06':    # jump-if-false opcode
                if self.intcode_list[parameters[0]] == 0:
                    self.index = self.intcode_list[parameters[1]]
                else:
                    self.index += 3
            elif opcode == '07':    # less than opcode
                if self.intcode_list[parameters[0]] < self.intcode_list[parameters[1]]:
                    try:
                        self.intcode_list[parameters[2]] = 1
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[2]] = 1
                else:
                    try:
                        self.intcode_list[parameters[2]] = 0
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[2]] = 0
                self.index += 4
            elif opcode == '08':    # equal opcode
                if self.intcode_list[parameters[0]] == self.intcode_list[parameters[1]]:
                    try:
                        self.intcode_list[parameters[2]] = 1
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[2]] = 1
                else:
                    try:
                        self.intcode_list[parameters[2]] = 0
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[2]] = 0
                self.index += 4
            elif opcode == '09':    # adjust relative base opcode
                self.relative_base += self.intcode_list[parameters[0]]
                self.index += 2
            elif opcode == '99':    # ending opcode
                self.nn_end = True
                print('IntCode computer execution terminated')
                break
            else:
                self.nn_end = True
                print('Error in compute_int_code')
                break

    def add_input(self, new_input: list):
        self.input_list.extend(new_input)

class ArcadeCabinet:
    def __init__(self, tiles_coords: list):
        self.tiles = self.identify_tiles_position(tiles_coords)

    def identify_tiles_position(self, input_list: list):
        output_list = []
        x = 0
        y = 0
        tile_type = 0

        for elem_idx in range(len(input_list)):
            if elem_idx % 3 == 0:
                x = input_list[elem_idx]
            elif elem_idx % 3 == 1:
                y = input_list[elem_idx]
            elif elem_idx % 3 == 2:
                tile_type = input_list[elem_idx]
                output_list.append([tile_type, (x, y)])
            else:
                print('Something has gone wrong in the identify_tiles_' +
                      'position function')

        return output_list

    def single_tile_type_repetitions(self, tile_type: int):
        return [type for type, _ in self.tiles if type == tile_type]

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

intcode_computer = IntCode(intcode_list=int_code)

while not intcode_computer.nn_end:
    intcode_computer.compute_int_code()

arcade = ArcadeCabinet(intcode_computer.output_list)
print(len(arcade.single_tile_type_repetitions(2)))

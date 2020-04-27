"""--- Day 13: Care Package - Part Two ---"""

import os
from copy import deepcopy
import time

class IntCode:
    index = 0
    relative_base = 0
    output_list = []
    nn_end = False

    def __init__(self,
                 intcode_list: list,
                 input_list: list = [],
                 set_mem_zero: int = None,
                 instance_id: int = 0):
        self.intcode_list = deepcopy(intcode_list)
        self.input_list = deepcopy(input_list)
        self.instance_id = instance_id
        if set_mem_zero:
            self.intcode_list[0] = set_mem_zero

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
                    try:
                        self.intcode_list[parameters[0]] = self.input_list[-1]
                    except:
                        self.expand_intcode_list(parameters)
                        self.intcode_list[parameters[0]] = self.input_list[-1]
                    self.input_list.pop()
                    self.index += 2
                else:
                    break              
            elif opcode == '04':    # output opcode
                self.index += 2
                try:
                    return self.intcode_list[parameters[0]]
                except:
                    self.expand_intcode_list(parameters)
                    return self.intcode_list[parameters[0]]
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
    JOYSTICK_POS = {
        'neutral': 0,
        'left': -1,
        'right': 1
    }

    def __init__(self,
                 tiles: dict = {},
                 score: int = 0,
                 init_joystick_pos: str = 'neutral'):
        self.tiles = deepcopy(tiles)
        self.score = score
        self.joystick_pos = self.JOYSTICK_POS[init_joystick_pos]
        if self.tiles:
            if self.single_tile_type_repetitions(2):
                self.blocks = True
            else:
                self.blocks = 'Still no blocks'
            if self.single_tile_type_repetitions(3):
                self.paddle = self.single_tile_type_repetitions(3).pop()
            else:
                self.paddle = None
            if self.single_tile_type_repetitions(4):
                self.ball = self.single_tile_type_repetitions(4).pop()
            else:
                self.ball = None
        else:
            self.blocks = 'Still no blocks'
            self.paddle = None
            self.ball = None
            
    def add_tile(self,
                 coords: tuple,
                 tile_type: int):
        self.tiles[coords] = tile_type
        if tile_type == 2 and self.blocks == 'Still no blocks':
            self.blocks == True
        elif self.blocks == True and not self.single_tile_type_repetitions(2):
            self.blocks = False
        elif tile_type == 3:
            self.paddle = coords
        elif tile_type == 4:
            self.ball = coords
        
        if self.ball and self.paddle:
            if self.ball[0] < self.paddle[0]:
                self.joystick_pos = self.JOYSTICK_POS['left']
            elif self.ball[0] > self.paddle[0]:
                self.joystick_pos = self.JOYSTICK_POS['right']
            else:
                self.joystick_pos = self.JOYSTICK_POS['neutral']

    def single_tile_type_repetitions(self, tile_type: int):
        return [coords for coords, tile_t in self.tiles.items() 
                                                    if tile_t == tile_type]

    def display_game(self):
        tile_type_dict = {
            0: ' ',
            1: '|',
            2: '□',
            3: '_',
            4: 'O',
        }

        min_x = min(x for x, _ in list(self.tiles))
        min_y = min(y for _, y in list(self.tiles))
        max_x = max(x for x, _ in list(self.tiles))
        max_y = max(y for _, y in list(self.tiles))

        output_string = ''
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):            
                if (x, y) in list(self.tiles):
                    output_string += tile_type_dict[self.tiles[(x, y)]]
                else:
                    output_string += ' '
            output_string += '\n'
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(output_string + str(self.score))
        time.sleep(0.00005)

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

intcode_computer = IntCode(intcode_list=int_code,
                           input_list=[0],
                           set_mem_zero=2)
arcade_cabinet = ArcadeCabinet()

while not intcode_computer.nn_end and arcade_cabinet.blocks:
    x = intcode_computer.compute_int_code()
    y = intcode_computer.compute_int_code()
    tile_type = intcode_computer.compute_int_code()
    if (x, y) == (-1, 0):
        arcade_cabinet.score = tile_type
    else:
        arcade_cabinet.add_tile((x, y), tile_type)
    intcode_computer.add_input([arcade_cabinet.joystick_pos])
    # arcade_cabinet.display_game()

print(arcade_cabinet.score)

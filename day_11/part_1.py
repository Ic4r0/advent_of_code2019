"""--- Day 11: Space Police - Part One ---"""

import os
import operator

class IntCode:
    index = 0
    relative_base = 0
    output_list = []
    nn_end = False

    def __init__(self,
                 intcode_list: list,
                 input_list: list,
                 instance_id: int = 0):
        self.intcode_list = intcode_list.copy()
        self.input_list = input_list.copy()
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
                print('Output: ', self.output_list[-1])
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

class Hull:
    panels_steps = []
    current_color = 0

    def __init__(self, 
                 starting_color: int = 0,           # black = 0, white = 1
                 starting_coords: tuple = (0, 0),   # coordinates [x, y]
                 starting_direction: str = 'up',
                 instance_id: int = 0):
        self.panels_steps.append([starting_color, starting_coords])
        self.direction = starting_direction
        self.instance_id = instance_id
    
    def check_prev_color(self, coords: tuple):
        old_occurences = [elem for elem in self.panels_steps
                                if elem[1] == coords]
        if old_occurences:
            if [0, coords] == old_occurences[-1]:
                return 0
            else:
                return 1
        else:
            return self.current_color

    def new_step(self, turn: int):
        if self.direction == 'up':
            if turn == 0:
                movement = (-1, 0)
                self.direction = 'left'
            elif turn == 1:
                movement = (1, 0)
                self.direction = 'right'
            else:
                print('Wrong turn')
        elif self.direction == 'down':
            if turn == 0:
                movement = (1, 0)
                self.direction = 'right'
            elif turn == 1:
                movement = (-1, 0)
                self.direction = 'left'
            else:
                print('Wrong turn')
        elif self.direction == 'left':
            if turn == 0:
                movement = (0, -1)
                self.direction = 'down'
            elif turn == 1:
                movement = (0, 1)
                self.direction = 'up'
            else:
                print('Wrong turn')
        elif self.direction == 'right':
            if turn == 0:
                movement = (0, 1)
                self.direction = 'up'
            elif turn == 1:
                movement = (0, -1)
                self.direction = 'down'
            else:
                print('Wrong turn')
        movement = tuple(map(operator.add, self.panels_steps[-1][1], movement))
        new_color = self.check_prev_color(movement)
        self.panels_steps.append([new_color, movement])

    def non_repeated_steps(self):
        return len(list(dict.fromkeys(
                        [elem for _, elem in self.panels_steps[:-1]]
                        )))


dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

ship_hull = Hull()
starting_color, _ = ship_hull.panels_steps[0]
intcode_computer = IntCode(intcode_list=int_code, input_list=[starting_color])

while not intcode_computer.nn_end:
    intcode_computer.compute_int_code()
    while intcode_computer.output_list:
        ship_hull.panels_steps[-1][0] = intcode_computer.output_list.pop(0)
        ship_hull.new_step(intcode_computer.output_list.pop(0))
    intcode_computer.add_input([ship_hull.panels_steps[-1][0]])

print(ship_hull.non_repeated_steps())

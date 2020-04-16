"""--- Day 11: Space Police - Part One ---"""

import os

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
        self.instance_id = intcode_id

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
            output_par = self.intcode_list[self.index + parameter_id + 1] +
                            self.relative_base
        else:
            print('Error in parameter_mode')
        return output_par

    def expand_intcode_list(self, index_out_of_bound: int):
        self.intcode_list.extend([0] * (index_out_of_bound -
                                        len(self.intcode_list) + 1))

    def compute_int_code(self):
        while(True):
            opcode, parameters = self.manage_opcode()
            if opcode == '01':      # add opcode
                pass
            elif opcode == '02':    # multiply opcode
                pass
            elif opcode == '03':    # input opcode
                pass
            elif opcode == '04':    # output opcode
                pass
            elif opcode == '05':    # jump-if-true opcode
                pass
            elif opcode == '06':    # jump-if-false opcode
                pass
            elif opcode == '07':    # less than opcode
                pass
            elif opcode == '08':    # equal opcode
                pass
            elif opcode == '09':    # adjust relative base opcode
                pass
            elif opcode == '99':    # ending opcode
                self.nn_end = True
                print('IntCode computer execution terminated')
                break
            else:
                self.nn_end = True
                print('Error in compute_int_code')
                break


dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

"""--- Day 7: Amplification Circuit - Part Two ---"""

import os
from itertools import permutations

def parameter_mode(int_stream: list,
                   idx: int,
                   opcode: str,
                   first_par: bool = True,
                   second_par: bool = True):
    output_first_par = None
    output_second_par = None
    # First parameter
    if first_par and int(opcode[2]) == 0:
        output_first_par = int_stream[int_stream[idx + 1]]
    else:
        output_first_par = int_stream[idx + 1]

    # Second parameter
    if second_par and int(opcode[1]) == 0:
        output_second_par = int_stream[int_stream[idx + 2]]
    else:
        output_second_par = int_stream[idx + 2]

    return output_first_par, output_second_par

def intcode_computer(int_stream: list,
                     first_input: int,
                     second_input: int,
                     index: int,
                     counter: int):
    # Amplifier's output signal
    amp_out_sig = None
    while int_stream[index] != 99 and index < len(int_stream):
        opcode = str(int_stream[index]).zfill(5)
        if int(opcode[-1]) == 1:    # add opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            int_stream[int_stream[index + 3]] = first_par + second_par
            index += 4
        elif int(opcode[-1]) == 2:  # multiply opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            int_stream[int_stream[index + 3]] = first_par * second_par
            index += 4
        elif int(opcode[-1]) == 3:  # input opcode
            counter += 1
            if counter == 1:
                int_stream[int_stream[index + 1]] = first_input
            else:
                int_stream[int_stream[index + 1]] = second_input
            index += 2
        elif int(opcode[-1]) == 4:  # output opcode
            first_par, _ = parameter_mode(int_stream, index, opcode, second_par=False)
            index += 2
            amp_out_sig = first_par
            break
        elif int(opcode[-1]) == 5:  # jump-if-true opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            if first_par != 0:
                index = second_par
            else:
                index += 3
        elif int(opcode[-1]) == 6:  # jump-if-false opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            if first_par == 0:
                index = second_par
            else:
                index += 3
        elif int(opcode[-1]) == 7:  # less than opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            if first_par < second_par:
                int_stream[int_stream[index + 3]] = 1
            else:
                int_stream[int_stream[index + 3]] = 0
            index += 4
        elif int(opcode[-1]) == 8:  # equal opcode
            first_par, second_par = parameter_mode(int_stream, index, opcode)
            if first_par == second_par:
                int_stream[int_stream[index + 3]] = 1
            else:
                int_stream[int_stream[index + 3]] = 0
            index += 4
    return amp_out_sig, index, counter

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

# Possible permutations of the phase settings
phase_settings = list(permutations(range(5, 10), 5))
# List of outputs
list_of_outputs = []

INPUT_SIGNAL = 0

for set_a, set_b, set_c, set_d, set_e in phase_settings:

    int_code_a = int_code.copy()
    int_code_b = int_code.copy()
    int_code_c = int_code.copy()
    int_code_d = int_code.copy()
    int_code_e = int_code.copy()
    
    idx_a, c_op_a = (0, 0)
    idx_b, c_op_b = (0, 0)
    idx_c, c_op_c = (0, 0)
    idx_d, c_op_d = (0, 0)
    idx_e, c_op_e = (0, 0)

    second_input_a = INPUT_SIGNAL
    single_output = None
    
    while int_code_e[idx_e] != 99 and idx_e < len(int_code_e):
        # Amplifier A
        second_input_b, idx_a, c_op_a = intcode_computer(int_code_a, first_input=set_a, second_input=second_input_a, index=idx_a, counter=c_op_a)
        # Amplifier B
        second_input_c, idx_b, c_op_b = intcode_computer(int_code_b, first_input=set_b, second_input=second_input_b, index=idx_b, counter=c_op_b)
        # Amplifier C
        second_input_d, idx_c, c_op_c = intcode_computer(int_code_c, first_input=set_c, second_input=second_input_c, index=idx_c, counter=c_op_c)
        # Amplifier D
        second_input_e, idx_d, c_op_d = intcode_computer(int_code_d, first_input=set_d, second_input=second_input_d, index=idx_d, counter=c_op_d)
        # Amplifier E
        second_input_a, idx_e, c_op_e = intcode_computer(int_code_e, first_input=set_e, second_input=second_input_e, index=idx_e, counter=c_op_e)
        if second_input_a:
            single_output = second_input_a
    
    list_of_outputs.append(single_output)

print(max(list_of_outputs))
     
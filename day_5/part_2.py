"""--- Day 5: Sunny with a Chance of Asteroids - Part Two ---"""

import os

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

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

INPUT = 5

# Start program
index = 0
while int_code[index] != 99 and index < len(int_code):
    opcode = str(int_code[index]).zfill(5)
    # print(opcode)

    if int(opcode[-1]) == 1:    # add opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        int_code[int_code[index + 3]] = first_par + second_par
        index += 4
    elif int(opcode[-1]) == 2:  # multiply opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        int_code[int_code[index + 3]] = first_par * second_par
        index += 4
    elif int(opcode[-1]) == 3:  # input opcode
        int_code[int_code[index + 1]] = INPUT
        index += 2
    elif int(opcode[-1]) == 4:  # output opcode
        first_par, _ = parameter_mode(int_code, index, opcode, second_par=False)
        print(first_par)
        index += 2
    elif int(opcode[-1]) == 5:  # jump-if-true opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        if first_par != 0:
            index = second_par
        else:
            index += 3
    elif int(opcode[-1]) == 6:  # jump-if-false opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        if first_par == 0:
            index = second_par
        else:
            index += 3
    elif int(opcode[-1]) == 7:  # less than opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        if first_par < second_par:
            int_code[int_code[index + 3]] = 1
        else:
            int_code[int_code[index + 3]] = 0
        index += 4
    elif int(opcode[-1]) == 8:  # equal opcode
        first_par, second_par = parameter_mode(int_code, index, opcode)
        if first_par == second_par:
            int_code[int_code[index + 3]] = 1
        else:
            int_code[int_code[index + 3]] = 0
        index += 4
    
"""--- Day 9: Sensor Boost - Part One ---"""

import os

def parameter_mode(int_stream: list,
                   idx: int,
                   opcode: str,
                   rel_base: int,
                   first_par: bool = True,
                   second_par: bool = True,
                   third_par: bool = True):
    output_first_par = None
    output_second_par = None
    output_third_par = None

    # First parameter
    if first_par and int(opcode[2]) == 0:
        try:
            output_first_par = int_stream[int_stream[idx + 1]]
        except:
            int_stream.extend([0] * (int_stream[idx + 1] - len(int_stream) + 1))
            output_first_par = int_stream[int_stream[idx + 1]]
    elif first_par and int(opcode[2]) == 1:
        output_first_par = int_stream[idx + 1]
    elif first_par and int(opcode[2]) == 2:
        try:
            output_first_par = int_stream[int_stream[idx + 1] + rel_base]
        except:
            int_stream.extend([0] * (int_stream[idx + 1] + rel_base - len(int_stream) + 1))
            output_first_par = int_stream[int_stream[idx + 1] + rel_base]

    # Second parameter
    if second_par and int(opcode[1]) == 0:
        try:
            output_second_par = int_stream[int_stream[idx + 2]]
        except:
            int_stream.extend([0] * (int_stream[idx + 2] - len(int_stream) + 1))
            output_second_par = int_stream[int_stream[idx + 2]]
    elif second_par and int(opcode[1]) == 1:
        output_second_par = int_stream[idx + 2]
    elif second_par and int(opcode[1]) == 2:
        try:
            output_second_par = int_stream[int_stream[idx + 2] + rel_base]
        except:
            int_stream.extend([0] * (int_stream[idx + 2] + rel_base - len(int_stream) + 1))
            output_second_par = int_stream[int_stream[idx + 2] + rel_base]

    # Third parameter
    if third_par and int(opcode[0]) == 0:
        output_third_par = int_stream[idx + 3]
    elif third_par and int(opcode[0]) == 2:
        output_third_par = int_stream[idx + 3] + rel_base

    return output_first_par, output_second_par, output_third_par

def intcode_computer(int_stream: list,
                     intcode_input: int):
    # Start program
    index = 0
    relative_base = 0
    while int_stream[index] != 99 and index < len(int_stream):
        opcode = str(int_stream[index]).zfill(5)
        if int(opcode[-1]) == 1:    # add opcode
            first_par, second_par, third_par = parameter_mode(int_stream, index, opcode, relative_base)
            try:
                int_stream[third_par] = first_par + second_par
            except:
                int_stream.extend([0] * (third_par - len(int_stream) + 1))
                int_stream[third_par] = first_par + second_par
            index += 4
        elif int(opcode[-1]) == 2:  # multiply opcode
            first_par, second_par, third_par = parameter_mode(int_stream, index, opcode, relative_base)
            try:
                int_stream[third_par] = first_par * second_par
            except:
                int_stream.extend([0] * (third_par - len(int_stream) + 1))
                int_stream[third_par] = first_par * second_par
            index += 4
        elif int(opcode[-1]) == 3:  # input opcode
            if int(opcode[2]) == 0:
                try:
                    int_stream[int_stream[index + 1]] = intcode_input
                except:
                    int_stream.extend([0] * (int_stream[index + 1] - len(int_stream) + 1))
                    int_stream[int_stream[index + 1]] = intcode_input
            elif int(opcode[2]) == 2:
                try:
                    int_stream[int_stream[index + 1] + relative_base] = intcode_input
                except:
                    int_stream.extend([0] * (int_stream[index + 1] + relative_base - len(int_stream) + 1))
                    int_stream[int_stream[index + 1] + relative_base] = intcode_input
            index += 2
        elif int(opcode[-1]) == 4:  # output opcode
            first_par, _, _ = parameter_mode(int_stream, index, opcode, relative_base, second_par=False, third_par=False)
            print(first_par)
            index += 2
        elif int(opcode[-1]) == 5:  # jump-if-true opcode
            first_par, second_par, _ = parameter_mode(int_stream, index, opcode, relative_base, third_par=False)
            if first_par != 0:
                index = second_par
            else:
                index += 3
        elif int(opcode[-1]) == 6:  # jump-if-false opcode
            first_par, second_par, _ = parameter_mode(int_stream, index, opcode, relative_base, third_par=False)
            if first_par == 0:
                index = second_par
            else:
                index += 3
        elif int(opcode[-1]) == 7:  # less than opcode
            first_par, second_par, third_par = parameter_mode(int_stream, index, opcode, relative_base)
            if first_par < second_par:
                try:
                    int_stream[third_par] = 1
                except:
                    int_stream.extend([0] * (third_par - len(int_stream) + 1))
                    int_stream[third_par] = 1
            else:
                try:
                    int_stream[third_par] = 0
                except:
                    int_stream.extend([0] * (third_par - len(int_stream) + 1))
            index += 4
        elif int(opcode[-1]) == 8:  # equal opcode
            first_par, second_par, third_par = parameter_mode(int_stream, index, opcode, relative_base)
            if first_par == second_par:
                try:
                    int_stream[third_par] = 1
                except:
                    int_stream.extend([0] * (third_par - len(int_stream) + 1))
                    int_stream[third_par] = 1
            else:
                try:
                    int_stream[third_par] = 0
                except:
                    int_stream.extend([0] * (third_par - len(int_stream) + 1))
            index += 4
        elif int(opcode[-1]) == 9:  # adjust relative base opcode
            first_par, _, _ = parameter_mode(int_stream, index, opcode, relative_base, second_par=False, third_par=False)
            relative_base += first_par
            index += 2

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

INPUT = 1

intcode_computer(int_stream=int_code, intcode_input=INPUT)

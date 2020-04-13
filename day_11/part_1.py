"""--- Day 11: Space Police - Part One ---"""

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

def movement(current_direction: str,
             previous_positions: list,
             output_param: int):
    curr_x, curr_y = previous_positions[-1][1]
    if current_direction == 'up':
        if output_param == 0:
            new_pos = (curr_x-1, curr_y)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'left'
        else:
            new_pos = (curr_x+1, curr_y)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'right'
    elif current_direction == 'down':
        if output_param == 0:
            new_pos = (curr_x+1, curr_y)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'right'
        else:
            new_pos = (curr_x-1, curr_y)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'left'
    elif current_direction == 'left':
        if output_param == 0:
            new_pos = (curr_x, curr_y-1)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'down'
        else:
            new_pos = (curr_x, curr_y+1)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'up'
    elif current_direction == 'right':
        if output_param == 0:
            new_pos = (curr_x, curr_y+1)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'up'
        else:
            new_pos = (curr_x, curr_y-1)
            if ['w', new_pos] in previous_positions:
                previous_positions.append(['w', new_pos])
            else:
                previous_positions.append(['b', new_pos])
            new_direction = 'down'
    return new_direction

def intcode_computer(int_stream: list):
    panels = [['b', (0, 0)]]
    direction = 'up'
    color_set = False

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
            if panels[-1][0] == 'b':
                input_value = 0
            else:
                input_value = 1
            if int(opcode[2]) == 0:
                try:
                    int_stream[int_stream[index + 1]] = input_value
                except:
                    int_stream.extend([0] * (int_stream[index + 1] - len(int_stream) + 1))
                    int_stream[int_stream[index + 1]] = input_value
            elif int(opcode[2]) == 2:
                try:
                    int_stream[int_stream[index + 1] + relative_base] = input_value
                except:
                    int_stream.extend([0] * (int_stream[index + 1] + relative_base - len(int_stream) + 1))
                    int_stream[int_stream[index + 1] + relative_base] = input_value
            index += 2
        elif int(opcode[-1]) == 4:  # output opcode
            first_par, _, _ = parameter_mode(int_stream, index, opcode, relative_base, second_par=False, third_par=False)
            if not color_set:
                if first_par == 0:
                    panels[-1][0] = 'b'
                else:
                    panels[-1][0] = 'w'
                color_set = True
            else:
                color_set = False
                direction = movement(direction, panels, first_par)

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
    return panels

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

steps_made = intcode_computer(int_stream=int_code)
# visited_panels = list(dict.fromkeys([elem for _, elem in steps_made]))
# print(len(visited_panels)-1)
print(steps_made)

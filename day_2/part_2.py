"""--- Day 2: 1202 Program Alarm - Part Two ---"""

import os

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    int_code = []
    for line in file:
        int_code.extend([int(elem) for elem in line.split(',')])

# Required output
output = 19690720

# List which contains all the possible noun-verb pairs
noun_verb_pairs = []
for i in range(100):
    for j in range(100):
        noun_verb_pairs.append((i, j))

# Test all possible pairs
for noun, verb in noun_verb_pairs:
    supp_int_code = int_code[:]
    supp_int_code[1] = noun
    supp_int_code[2] = verb
    index = 0
    while supp_int_code[index] != 99 and index < len(supp_int_code):
        if supp_int_code[index] == 1:
            supp_int_code[supp_int_code[index + 3]] = supp_int_code[supp_int_code[index + 1]] + \
                                                      supp_int_code[supp_int_code[index + 2]]
        elif int_code[index] == 2:
            supp_int_code[supp_int_code[index + 3]] = supp_int_code[supp_int_code[index + 1]] * \
                                                      supp_int_code[supp_int_code[index + 2]]
        index += 4
    # If the first element of the number list is equal to the required output then stop
    if supp_int_code[0] == output:
        print('noun: ', noun)
        print('verb: ', verb)
        print(100 * noun + verb)
        break

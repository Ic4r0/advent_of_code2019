"""--- Day 14: Space Stoichiometry - Part Two ---"""

import os
import re
from copy import deepcopy

class Reaction:

    def __init__(self, reactions: dict):
        self.reactions = deepcopy(reactions)
    
    def ore_cost_for_elem(self,
                          qnt_elem: int,
                          elem: str,
                          start_remains: dict = {}):
        ore_needed = 0
        op_chem, in_chem = [(k, v) for k, v in self.reactions.items()
                                                        if k[1] == elem].pop()
        if op_chem[0] < qnt_elem:
            multiplier = qnt_elem // op_chem[0] + (qnt_elem % op_chem[0] > 0)
            in_chem = [(multiplier*k, v) for k, v in in_chem]
            if op_chem[0] * multiplier > qnt_elem:
                start_remains[op_chem[1]] = op_chem[0] * multiplier - qnt_elem
        elif op_chem[0] > qnt_elem:
            start_remains[op_chem[1]] = op_chem[0] - qnt_elem
        
        if 'ORE' in [v for _, v in in_chem]:
            ore_needed += sum([qnt for qnt, elem in in_chem if elem == 'ORE'])
        else:
            for qnt, elem in in_chem:
                if elem in start_remains:
                    if qnt < start_remains[elem]:
                        start_remains[elem] -= qnt
                    elif qnt == start_remains[elem]:
                        start_remains.pop(elem, 0)
                    else:
                        ore_needed += self.ore_cost_for_elem(qnt - start_remains.pop(elem, 0), 
                                                             elem,
                                                             start_remains)
                else:
                    ore_needed += self.ore_cost_for_elem(qnt, elem, start_remains)
        
        return ore_needed

dirname, _ = os.path.split(os.path.abspath(__file__))
file_path = dirname + "\\input"

# Open the input file
with open(file_path) as file:
    # Create a list where we store each element of the input
    reaction_dict = {}
    for line in file:
        match = re.findall(r"(\d+ \w+)", line)
        output_chemical = tuple(match.pop().split())
        output_chemical = (int(output_chemical[0]), output_chemical[1])
        input_chemical = [tuple(elem.split()) for elem in match]
        for idx in range(len(input_chemical)):
            qnt, element = input_chemical[idx]
            input_chemical[idx] = (int(qnt), element)
        reaction_dict[output_chemical] = input_chemical

reaction = Reaction(reaction_dict)
result_from_part_1 = reaction.ore_cost_for_elem(1, 'FUEL')

given_ore = 1000000000000

min_fuel_value = 0
max_fuel_value = given_ore

while min_fuel_value < max_fuel_value - 1:
    mid_fuel_value = (max_fuel_value + min_fuel_value) // 2
    ore_used = reaction.ore_cost_for_elem(mid_fuel_value, 'FUEL', {'ORE': given_ore})
    if ore_used < given_ore:
        min_fuel_value = mid_fuel_value
    elif ore_used > given_ore:
        max_fuel_value = mid_fuel_value - 1
    else:
        break

print(mid_fuel_value)
# print(reaction.ore_cost_for_elem(mid_fuel_value-1, 'FUEL', {'ORE': given_ore}))
# print(reaction.ore_cost_for_elem(mid_fuel_value, 'FUEL', {'ORE': given_ore}))
# print(reaction.ore_cost_for_elem(mid_fuel_value+1, 'FUEL', {'ORE': given_ore}))

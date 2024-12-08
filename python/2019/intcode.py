import logging
import sys
from typing import List, Union

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

####################
# Global registers #
####################
eip = 0
base_offset = 0

##########################
# Parameter mode helpers #
##########################
def is_immediate(modestring: Union[int,str]) -> bool:
    return str(modestring) == '1'

def is_relative(modestring: Union[int,str]) -> bool:
    return str(modestring) == '2'

def get_param(program, location, modestring: Union[int,str], write=False) -> int:
    global base_offset

    if is_immediate(modestring):
        return program[location]
    elif is_relative(modestring):
        return program[base_offset + program[location]]
    else:
        return program[program[location]]

##############
# Operations #
##############
def addition(program, mode_one, mode_two, mode_three):
    global eip
    operand_one = get_param(program, eip+1, mode_one)
    operand_two = get_param(program, eip+2, mode_two)
    logging.debug("{} (ADD) {} {} -> {}: ".format(program[eip], program[eip+1], program[eip+2], program[eip+3]))
    dest_addr = base_offset + program[eip+3] if is_relative(mode_three) else program[eip+3]
    program[dest_addr] = operand_one + operand_two
    eip = eip + 4


def multiplication(program, mode_one, mode_two, mode_three):
    global eip
    operand_one = get_param(program, eip+1, mode_one)
    operand_two = get_param(program, eip+2, mode_two)
    logging.debug("{} (MUL) {} {} -> {}: ".format(program[eip], program[eip+1], program[eip+2], program[eip+3]))
    dest_addr = base_offset + program[eip+3] if is_relative(mode_three) else program[eip+3]
    program[dest_addr] = operand_one * operand_two
    eip = eip + 4


def input_instruction(program, mode_one):
    global eip
    logging.debug("{} (INPUT) -> {}: ".format(program[eip], program[eip+1]))
    print("Offset: {}".format(base_offset))
    dest_addr = base_offset + program[eip+1] if is_relative(mode_one) else program[eip+1]
    program[dest_addr] = int(input("Input value for opcode 3: "))
    eip = eip + 2


def output(program, mode_one):
    global eip
    logging.debug("{} (OUTPUT) {}: ".format(program[eip], program[eip+1]))
    output = get_param(program, eip+1, mode_one)
    print("Output: {}".format(output))
    eip = eip + 2


def jump_if_true(program, mode_one, mode_two):
    global eip
    logging.debug("{} (JT) {} {}: ".format(program[eip], program[eip+1], program[eip+2]))
    argument = get_param(program, eip+1, mode_one)
    jump_target = get_param(program, eip+2, mode_two)
    if argument != 0:
        eip = jump_target
    else:
        eip = eip + 3


def jump_if_false(program, mode_one, mode_two):
    global eip
    logging.debug("{} (JF) {} {}: ".format(program[eip], program[eip+1], program[eip+2]))
    argument = get_param(program, eip+1, mode_one)
    jump_target = get_param(program, eip+2, mode_two)
    if argument == 0:
        eip = jump_target
    else:
        eip = eip + 3


def less_than(program, mode_one, mode_two, mode_three):
    global eip
    logging.debug("{} (LT) {} {} -> {}: ".format(program[eip], program[eip+1], program[eip+2], program[eip+3]))
    left_side = get_param(program, eip+1, mode_one)
    right_side = get_param(program, eip+2, mode_two)
    dest_addr = base_offset + program[eip+3] if is_relative(mode_three) else program[eip+3]
    program[dest_addr] = 1 if left_side < right_side else 0
    eip = eip + 4


def equals(program, mode_one, mode_two, mode_three):
    global eip
    logging.debug("{} (EQ) {} {} -> {}: ".format(program[eip], program[eip+1], program[eip+2], program[eip+3]))
    left_side = get_param(program, eip+1, mode_one)
    right_side = get_param(program, eip+2, mode_two)
    dest_addr = base_offset + program[eip+3] if is_relative(mode_three) else program[eip+3]
    program[dest_addr] = 1 if left_side == right_side else 0
    eip = eip + 4


def relative_base_offset(program, mode_one):
    global eip
    global base_offset
    logging.debug("{} (RBO) {}: before: {} after: {}".format(program[eip], program[eip+1], base_offset, base_offset+get_param(program,eip+1,mode_one)))
    base_offset = base_offset + get_param(program, eip+1, mode_one)
    eip = eip + 2


############
# Dispatch #
############
def execute(program: List[int]) -> List[int]:
    global eip
    global base_offset
    while eip < len(program):
        # parse opcode
        full_opcode = str(program[eip]).zfill(5)
        opcode = full_opcode[3:]
        mode_one = full_opcode[2]
        mode_two = full_opcode[1]
        mode_three = full_opcode[0]

        # perform op
        if int(opcode) == 1:
            addition(program, mode_one, mode_two, mode_three)
        elif int(opcode) == 2:  # multiplication
            multiplication(program, mode_one, mode_two, mode_three)
        elif int(opcode) == 3:  # input
            input_instruction(program, mode_one)
        elif int(opcode) == 4:  # output
            output(program, mode_one)
        elif int(opcode) == 5:  # jump if true
            jump_if_true(program, mode_one, mode_two)
        elif int(opcode) == 6:  # jump if false
            jump_if_false(program, mode_one, mode_two)
        elif int(opcode) == 7:  # less than
            less_than(program, mode_one, mode_two, mode_three)
        elif int(opcode) == 8:  # equals
            equals(program, mode_one, mode_two, mode_three)
        elif int(opcode) == 9:  # rbo
            relative_base_offset(program, mode_one)
        elif int(opcode) == 99:  # halt
            break
        else:
            raise Exception("Got invalid opcode {}".format(full_opcode))

    return program

if __name__ == "__main__":
    assert len(sys.argv) > 1

    program = ""
    with open(sys.argv[1]) as f:
        program = f.read().strip().split(',')

    # make everything into ints
    program = [int(p) for p in program]
    # throw on some spare memory for day9
    program.extend([0 for i in range(100)])

    print("Final program state {}".format(execute(program)))

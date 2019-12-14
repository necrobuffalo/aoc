import sys
from typing import List

def execute(program: List[int]) -> List[int]:
    eip = 0
    while eip < len(program):
        # parse opcode
        full_opcode = str(program[eip]).zfill(5)
        opcode = full_opcode[3:]
        mode_one = full_opcode[2] == '1'
        mode_two = full_opcode[1] == '1'
        mode_three = full_opcode[0] == '1'

        # perform op
        if int(opcode) == 1:
            operand_one = program[eip+1] if mode_one else program[program[eip+1]]
            operand_two = program[eip+2] if mode_two else program[program[eip+2]]
            program[program[eip+3]] = operand_one + operand_two
            eip = eip + 4
        elif int(opcode) == 2:  # multiplication
            operand_one = program[eip+1] if mode_one else program[program[eip+1]]
            operand_two = program[eip+2] if mode_two else program[program[eip+2]]
            program[program[eip+3]] = operand_one * operand_two
            eip = eip + 4
        elif int(opcode) == 3:  # input
            program[program[eip+1]] = int(input("Input value for opcode 3: "))
            eip = eip + 2
        elif int(opcode) == 4:  # output
            output = program[eip+1] if mode_one else program[program[eip+1]]
            print("Output: {}".format(output))
            eip = eip + 2
        elif int(opcode) == 5:  # jump if true
            argument = program[eip+1] if mode_one else program[program[eip+1]]
            jump_target = program[eip+2] if mode_two else program[program[eip+2]]
            if argument != 0:
                eip = jump_target
            else:
                eip = eip + 3
        elif int(opcode) == 6:  # jump if false
            argument = program[eip+1] if mode_one else program[program[eip+1]]
            jump_target = program[eip+2] if mode_two else program[program[eip+2]]
            if argument == 0:
                eip = jump_target
            else:
                eip = eip + 3
        elif int(opcode) == 7:  # less than
            left_side = program[eip+1] if mode_one else program[program[eip+1]]
            right_side = program[eip+2] if mode_two else program[program[eip+2]]
            program[program[eip+3]] = 1 if left_side < right_side else 0
            eip = eip + 4
        elif int(opcode) == 8:  # equals
            left_side = program[eip+1] if mode_one else program[program[eip+1]]
            right_side = program[eip+2] if mode_two else program[program[eip+2]]
            program[program[eip+3]] = 1 if left_side == right_side else 0
            eip = eip + 4
        elif int(opcode) == 99:
            break

    return program

if __name__ == "__main__":
    assert len(sys.argv) > 1

    program = ""
    with open(sys.argv[1]) as f:
        program = f.read().strip().split(',')

    # make everything into ints
    program = [int(p) for p in program]

    print("Final program state {}".format(execute(program)))

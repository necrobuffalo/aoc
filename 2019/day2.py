from typing import List
def execute(program: List[int], pos_one: int = 12, pos_two: int = 2) -> List[int]:
    # Make required program changes:
    program[1] = pos_one
    program[2] = pos_two

    eip = 0
    while eip < len(program):
        assert program[eip] in [1, 2, 99]

        # Process opcodes
        if program[eip] == 99:
            # hit 99, halt execution here
            break
        elif program[eip] == 1:
            left_pos, right_pos, dest = program[eip+1:eip+4]
            program[dest] = program[left_pos] + program[right_pos]
        elif program[eip] == 2:
            left_pos, right_pos, dest = program[eip+1:eip+4]
            program[dest] = program[left_pos] * program[right_pos]
        else:
            raise Exception("Got invalid opcode!")

        # Step to next instruction
        eip = eip + 4

    return program

def part2(program: List[int]) -> None:
    desired_output = 19690720

    for noun in range(100):
        for verb in range(100):
            try:
                test_case = execute(program.copy(), noun, verb)
            except Exception:
                continue

            if test_case[0] == desired_output:
                print("Found with verb={},noun={}".format(noun, verb))
                print("{}".format(100 * noun + verb))
                break

# Dump everything in a list
program = input()
# Split and convert to ints
program = [int(i) for i in program.split(',')]

print("Final part1 intcode program state: {}".format(execute(program.copy())))
part2(program.copy())

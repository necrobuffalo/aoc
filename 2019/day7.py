from itertools import permutations
from multiprocessing import Pool
import sys
from typing import List

import pexpect

from intcode import execute

DEFAULT_CONCURRENCY = 30


def single_circuit(phases: str) -> int:
    print("Trying {}.".format(phases))
    processes = [pexpect.spawn('python intcode.py {}'.format(sys.argv[2])) for i in range(5)]

    next_input = '0'
    for i in range(len(processes)):
        # Input phase
        processes[i].expect("Input value for opcode 3: ")
        processes[i].sendline(phases[i])
        # Input signal
        processes[i].expect("Input value for opcode 3: ")
        processes[i].sendline(next_input)
        # Grab the input for the next process
        processes[i].expect("Output: ")
        next_input = processes[i].readline().strip()

    # Final value of next_input is our max signal
    return int(next_input)


def feedback_loop(phases: str) -> int:
    print("Trying {}.".format(phases))
    # Start all our child processes
    processes = [pexpect.spawn('python intcode.py {}'.format(sys.argv[2])) for i in range(5)]

    # Input phase settings for all amplifiers
    for i in range(len(processes)):
        processes[i].expect("Input value for opcode 3: ")
        processes[i].sendline(phases[i])

    # Loop until everything halts
    current_process = 0
    next_input = '0'
    while processes[current_process].isalive():
        processes[current_process].expect("Input value for opcode 3: ")
        processes[current_process].sendline(next_input)
        processes[current_process].expect("Output: ")
        next_input = processes[current_process].readline().strip()
        # Move to the next in the loop
        current_process = (current_process + 1) % len(processes)

    return int(next_input)


def part_one(concurrency=DEFAULT_CONCURRENCY):
    possible_arguments = [''.join(p) for p in permutations('01234')]
    signal_strengths = []
    with Pool(concurrency) as p:
        signal_strengths = p.map(single_circuit, possible_arguments)

    max_signal = max(signal_strengths)
    print("Max signal is {}".format(max_signal))


def part_two(concurrency=DEFAULT_CONCURRENCY):
    possible_arguments = [''.join(p) for p in permutations('56789')]
    signal_strengths = []
    with Pool(concurrency) as p:
        signal_strengths = p.map(feedback_loop, possible_arguments)

    print("Max signal: {}".format(max(signal_strengths)))


if __name__ == '__main__':
    assert len(sys.argv) > 2
    if sys.argv[1] == '1':
        part_one()
    else:
        part_two()

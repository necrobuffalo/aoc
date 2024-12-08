from math import floor

from typing import List

def fuel_for_mass(mass: int) -> int:
    return floor(mass / 3.0) - 2

def fuel_for_mass_and_fuel(mass: int) -> int:
    total_fuel = fuel_for_mass(mass)
    fuel_for_fuel = fuel_for_mass(total_fuel)
    while fuel_for_fuel > 0:
        total_fuel = total_fuel + fuel_for_fuel
        fuel_for_fuel = fuel_for_mass(fuel_for_fuel)
    return total_fuel

def part1(lines: List[str]) -> int:
    # Calculate base fuel
    base_fuel = 0
    for l in lines:
        base_fuel = base_fuel + fuel_for_mass(int(l))
    return base_fuel


def part2(lines: List[str]) -> int:
    base_fuel = 0
    for l in lines:
        base_fuel = base_fuel + fuel_for_mass_and_fuel(int(l))
    return base_fuel



# Dump everything in a list
lines = []
try:
    while True:
        lines.append(input())
except EOFError:
    pass

# Strip newlines
lines = [l for l in lines if l != '']
print(lines)

print("Total base fuel: {}".format(part1(lines)))
print("Total base fuel (including extra fuel to support fuel mass): {}".format(part2(lines)))

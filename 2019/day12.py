from itertools import combinations
import re
import sys
from typing import List, Tuple

moon_pattern = re.compile(r'<x=(?P<x>-?\d+),\s*y=(?P<y>-?\d+),\s*z=(?P<z>-?\d+)>')

class Velocity(object):
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return 'Velocity({},{},{})'.format(self.x,self.y,self.z)

    def kinetic_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon(object):
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        self.velocity = Velocity(0,0,0)

    def __str__(self):
        return 'Moon({},{},{},{})'.format(self.x,self.y,self.z,self.velocity)

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return self.velocity.kinetic_energy()

    def velocity_step(self):
        self.x = self.x + self.velocity.x
        self.y = self.y + self.velocity.y
        self.z = self.z + self.velocity.z


def parse_moon(line: str) -> Moon:
    m = re.match(moon_pattern, line).groupdict()
    return Moon(int(m['x']), int(m['y']), int(m['z']))

def apply_gravity(m: Tuple[Moon, Moon]):
    m1 = m[0]
    m2 = m[1]
    if m1.x > m2.x:
        m1.velocity.x = m1.velocity.x - 1
        m2.velocity.x = m2.velocity.x + 1
    elif m1.x < m2.x:
        m1.velocity.x = m1.velocity.x + 1
        m2.velocity.x = m2.velocity.x - 1

    if m1.y > m2.y:
        m1.velocity.y = m1.velocity.y - 1
        m2.velocity.y = m2.velocity.y + 1
    elif m1.y < m2.y:
        m1.velocity.y = m1.velocity.y + 1
        m2.velocity.y = m2.velocity.y - 1

    if m1.z > m2.z:
        m1.velocity.z = m1.velocity.z - 1
        m2.velocity.z = m2.velocity.z + 1
    elif m1.z < m2.z:
        m1.velocity.z = m1.velocity.z + 1
        m2.velocity.z = m2.velocity.z - 1

def gravity_step(moons: List[Moon]):
    for c in combinations(moons, 2):
        apply_gravity(c)


def simulate_n(moons: List[Moon], steps=1000):
    for i in range(0,steps):
        gravity_step(moons)
        for m in moons:
            m.velocity_step()
    total_energy = sum(map(lambda m: m.kinetic_energy() * m.potential_energy(), moons))
    print(total_energy)

if __name__ == '__main__':
    assert len(sys.argv) > 1

    with open(sys.argv[1]) as f:
        raw_moons = f.read().splitlines()

    moons = []
    for m in raw_moons:
        moons.append(parse_moon(m))

    simulate_n(moons)

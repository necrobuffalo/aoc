from collections import namedtuple
import math
import sys
from typing import List

Point = namedtuple('Point', ['x', 'y'])


def is_collinear(a: Point, b: Point, c: Point) -> bool:
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) == 0


def is_between(a: Point, b: Point, c: Point) -> bool:
    """
    Returns true if c is between a and b
    """
    return (a.x <= c.x <= b.x or b.x <= c.x <= a.x) and (a.y <= c.y <= b.y or b.y <= c.y <= a.y)


def is_visible_from(base: Point, target: Point, field: List[Point]) -> bool:
    """
    True if target/base are visible from each other
    """
    # an asteroid is not visible from itself
    if base == target:
        return False

    for a in field:
        if a != base and a != target and is_collinear(base, target, a) and is_between(base, target, a):
            # a blocks base's view of target, so this asteroid isn't visible.
            return False
    # Nothing blocked this asteroid, so return true.
    return True

def angle_from(base: Point, target: Point) -> float:
    """
    Returns this asteroid's angle compared to the y axis, ie if the laser is at base,
    how many degrees must it rotate to hit target?
    """
    # should be something like tan-1(x/y), but remember to adjust for which quadrant.
    relative_x = target.x - base.x
    relative_y = target.y - base.y
    tangent = math.atan(relative_x/relative_y) if relative_y != 0 else 0

    if relative_x==0 and relative_y > 0:
        # straight down
        return 180.0
    elif relative_x==0 and relative_y < 0:
        # straight up
        return 0.0
    elif relative_x > 0 and relative_y==0:
        # straight right
        return 90.0
    elif relative_x < 0 and relative_y==0:
        # straight left
        return 270.0
    elif relative_y > 0:
        # lower right/left
        return 180.0 + tangent
    elif relative_x > 0 and relative_y < 0:
        # upper right
        return abs(tangent)
    elif relative_x < 0 and relative_y < 0:
        # upper left
        return 360.0 - tangent

    return 0.0

def distance(base: Point, target: Point) -> float:
    relative_x = target.x - base.x
    relative_y = target.y - base.y
    return math.sqrt(math.pow(relative_x,2) + math.pow(relative_y,2))


def part_one(asteroid_list: List[Point]):
    # make an empty adjacency list of which asteroids are visible from where
    asteroid_graph = {a: set() for a in asteroid_list}

    for src in asteroid_graph.keys():
        for dest in asteroid_graph.keys():
            if is_visible_from(src, dest, asteroid_graph.keys()):
                asteroid_graph[src].add(dest)

    most_visible = max(asteroid_graph, key=lambda a: len(asteroid_graph[a]))
    print("Most visible: {} from {}".format(len(asteroid_graph[most_visible]), most_visible))


def part_two(asteroid_list: List[Point]):
    base = Point(11,11)  # from part one
    asteroid_list.remove(base)
    angles = {a: angle_from(base, a) for a in asteroid_list}
    distances = {a: distance(base, a) for a in asteroid_list}
    # Setting the laser angle to a negative value so that on the first iteration, we'll fire
    # on an asteroid with angle 0.0. Angles are calculated going all the way around clockwise
    # from the Y axis, so we should never have an asteroid at a negative angle and this
    # won't cause us to fire on an asteroid earlier than we should.
    laser_angle = -1.0
    asteroids_destroyed = 0

    while len(angles) > 0:
        # Anything where the angle is greater than the current angle is a valid move.
        possible_next_moves = [p for p in angles if angles[p] > laser_angle]

        if len(possible_next_moves) == 0:
            # we've rotated all the way around, reset the laser angle.
            laser_angle = -1.0
            print("full rotation completed, remaining: {}".format(angles))
            continue

        # what's the next angle we can fire at?
        next_angle = angles[min(possible_next_moves, key=lambda p: angles[p])]
        # filter even more to just this angle
        asteroids_in_line = [p for p in possible_next_moves if angles[p] == next_angle]
        # now find whichever one's the closest, and "destroy" it
        closest_asteroid = min(asteroids_in_line, key=lambda p: distances[p])
        asteroids_destroyed = asteroids_destroyed + 1
        print("{}: fired on {} at angle {}, distance {}".format(asteroids_destroyed, closest_asteroid, angles[closest_asteroid], distances[closest_asteroid]))
        del angles[closest_asteroid]
        del distances[closest_asteroid]

        # update the laser angle
        laser_angle = next_angle

assert len(sys.argv) > 1

with open(sys.argv[1]) as f:
    asteroid_field = f.read().splitlines()

asteroid_list = [Point(x,y) for x in range(len(asteroid_field[0])) for y in range(len(asteroid_field)) if asteroid_field[y][x] == '#']

part_two(asteroid_list)

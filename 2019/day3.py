from collections import namedtuple
from typing import List, Set, Tuple

Point = namedtuple('Point', ['x', 'y'])

def mark_path(wire: List[str]) -> Set[Tuple[Point]]:
    """
    Trace a wire and return the set of all points it visits.
    """
    position = Point(0, 0)
    marked_points = set()
    marked_points.add(position)
    for item in wire:
        direction = item[0]
        distance = int(item[1:])
        assert direction in ['U','D','L','R']

        if direction == 'U':
            coords = [Point(position.x,y) for y in range(position.y, position.y+distance+1)]
            marked_points.update(coords)
            position = position._replace(y=position.y + distance)
        elif direction == 'D':
            coords = [Point(position.x,y) for y in range(position.y-distance, position.y)]
            marked_points.update(coords)
            position = position._replace(y=position.y - distance)
        elif direction == 'L':
            coords = [Point(x,position.y) for x in range(position.x-distance, position.x)]
            marked_points.update(coords)
            position = position._replace(x=position.x - distance)
        elif direction == 'R':
            coords = [Point(x,position.y) for x in range(position.x, position.x+distance+1)]
            marked_points.update(coords)
            position = position._replace(x=position.x + distance)

    return marked_points

def manhattan_distance(p: Point) -> int:
    return abs(p.x) + abs(p.y)

def distance_along_path(wire: List[str], p: Point) -> int:
    position = Point(0, 0)
    steps = 0
    for item in wire:
        direction = item[0]
        distance = int(item[1:])
        assert direction in ['U','D','L','R']

        if direction == 'U':
            if p.x == position.x and (position.y <= p.y <= position.y+distance):
                # print("Found intersection {} tracing {}{} from {}".format(p,direction,distance,position))
                # print("Adding distance: {}".format(p.y - position.y))
                return steps + abs(p.y - position.y)
            # Update our current position
            position = position._replace(y=position.y + distance)
        elif direction == 'D':
            if p.x == position.x and (position.y-distance <= p.y <= position.y):
                # print("Found intersection {} tracing {}{} from {}".format(p,direction,distance,position))
                # print("Adding distance: {}".format(p.y - position.y))
                return steps + abs(p.y - position.y)
            # Update our current position
            position = position._replace(y=position.y - distance)
        elif direction == 'L':
            if p.y == position.y and (position.x-distance <= p.x <= position.x):
                # print("Found intersection {} tracing {}{} from {}".format(p,direction,distance,position))
                # print("Adding distance: {}".format(p.x - position.x))
                return steps + abs(p.x - position.x)
            # Update our current position
            position = position._replace(x=position.x - distance)
        elif direction == 'R':
            if p.y == position.y and (position.x <= p.x <= position.x+distance):
                # print("Found intersection {} tracing {}{} from {}".format(p,direction,distance,position))
                # print("Adding distance: {}".format(p.x - position.x))
                return steps + abs(p.x - position.x)
            # Update our current position
            position = position._replace(x=position.x + distance)

        steps = steps + distance

    return -1

wire_one = input().split(',')
wire_two = input().split(',')

path_one = mark_path(wire_one)
path_two = mark_path(wire_two)
# print(path_one)
# print(path_two)

intersections = path_one & path_two
intersections.remove(Point(0,0))
print("Found {} intersections".format(len(intersections)))
distances = [manhattan_distance(p) for p in intersections]
print("Min manhattan distance: {}".format(min(distances)))

# Now to find the first intersection
distances = []
for i in intersections:
    first_distance = distance_along_path(wire_one, i)
    second_distance = distance_along_path(wire_two, i)
    print("Distance to {}: {}+{}={}".format(i, first_distance, second_distance, first_distance + second_distance))
    distances.append(first_distance + second_distance)

print("Min distance along wire: {}".format(min(distances)))

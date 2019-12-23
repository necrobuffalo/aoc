from collections import namedtuple
from enum import IntEnum
import sys
from typing import Dict

import pexpect

# Some helpful types
Point = namedtuple('Point', ['x', 'y'])

class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

class RobotFacing(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Color(IntEnum):
    BLACK = 0
    WHITE = 1

def render_panels(panels: Dict[Point, int]):
    left_edge = min([p.x for p in panels])
    right_edge = max([p.x for p in panels])
    bottom_edge = min([p.y for p in panels])
    top_edge = max([p.y for p in panels])

    color_map = {0: ' ', 1: '#'}

    for y in reversed(range(bottom_edge,top_edge+1)):
        for x in range(left_edge,right_edge+1):
            p = Point(x,y)
            if p in panels:
                print(color_map[panels[p]], end='')
            else:
                print(color_map[0], end='')
        print()

assert len(sys.argv) > 1

robot_computer = pexpect.spawn('python intcode.py {}'.format(sys.argv[1]))

panels = dict()
robot_location = Point(0,0)
robot_direction = RobotFacing.UP

# start off over a black panel, provide 0
robot_computer.expect("Input value for opcode 3: ")
#robot_computer.sendline(str(int(Color.BLACK)))
robot_computer.sendline(str(int(Color.WHITE)))

while robot_computer.isalive():
    # Paint the square
    robot_computer.expect("Output: ")
    next_color = int(robot_computer.readline().strip())
    panels[robot_location] = next_color
    print("Painting {} color {}".format(robot_location, next_color))

    # Turn the robot
    robot_computer.expect("Output: ")
    next_direction = int(robot_computer.readline().strip())
    if next_direction == Direction.LEFT:
        robot_direction = robot_direction - 1 if robot_direction > RobotFacing.UP else RobotFacing.LEFT
    elif next_direction == Direction.RIGHT:
        robot_direction = robot_direction + 1 if robot_direction < RobotFacing.LEFT else RobotFacing.UP

    # Move the robot forward
    if robot_direction == RobotFacing.UP:
        robot_location = Point(robot_location.x, robot_location.y+1)
    elif robot_direction == RobotFacing.RIGHT:
        robot_location = Point(robot_location.x+1, robot_location.y)
    elif robot_direction == RobotFacing.DOWN:
        robot_location = Point(robot_location.x, robot_location.y-1)
    elif robot_direction == RobotFacing.LEFT:
        robot_location = Point(robot_location.x-1, robot_location.y)

    # Input the color of the current square
    if robot_location in panels:
        robot_computer.sendline(str(panels[robot_location]))
    else:
        # Any square we haven't visited will be black.
        robot_computer.sendline(str(int(Color.BLACK)))

print("Painted {} panels.".format(len(panels)))
render_panels(panels)

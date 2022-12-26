import sys
sys.path.append('../util')
import util

import copy
import time
from enum import Enum

# https://adventofcode.com/2022/day/24

lines = []
grid = []
grid_loop = []

Wind = Enum('Wind', ['EXIT', 'RIGHT',  'DOWN',  'UP', 'LEFT', 'WAIT', ])

class Node:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_wind(c):
    if c=='.':
        return set()

    d = {
        '^': Wind.UP,
        'v': Wind.DOWN,
        '<': Wind.LEFT,
        '>': Wind.RIGHT,
    }
    return set([d[c]])

def get_grid(lines):
    grid = []
    for line in lines:
        if line[2] == '#':
            continue

        grid_line = []
        for cell in line:
            if cell == '#':
                continue

            grid_line.append(get_wind(cell))

        grid.append(grid_line)

    return grid

def cp(c):
    cc = c.copy()
    d = {
        Wind.UP: '^',
        Wind.DOWN: 'v',
        Wind.LEFT: '<',
        Wind.RIGHT: '>'
    }
    assert len(cc) == 1
    return(d[cc.pop()])

class Grid:
    __slots__ = ['grid', 'wx', 'wy', 'time_nodes']

    def __init__(self, grid):
        self.grid = grid
        self.wx = len(self.grid[0])
        self.wy = len(self.grid)
        self.time_nodes = [[(0, -1, 0)]]

    def print(self):
        for y,gl in enumerate(self.grid):
            for x,c in enumerate(gl):
                if x==self.x and y==self.y:
                    print('*', end='')
                elif len(c) == 0:
                    print('.', end='')
                elif len(c) == 1:
                    print(cp(c), end='')
                else:
                    print(len(c), end='')
            print()
        print('-------------------------------')

    def can_move_time(self, y, x, time):
        # Look right for left winds
        xr = (x + time) % self.wx
        if Wind.LEFT in self.grid[y][xr]:
            return False

        # Look left for right winds
        xl = (x - time) % self.wx
        if Wind.RIGHT in self.grid[y][xl]:
            return False

        # Look up for down winds
        yu = (y - time) % self.wy
        if Wind.DOWN in self.grid[yu][x]:
            return False

        # Look down ...
        yd = (y+time) % self.wy
        if Wind.UP in self.grid[yd][x]:
            return False

        return True

    def can_moves(self, node, time):
        can = []

        if node.y == self.wy -1 and node.x == self.wx-1:
            can.append(Wind.EXIT)
            return can

        if node.x < self.wx-1 and self.can_move_time(node.y, node.x + 1, time) and node.y >= 0:
            can.append(Wind.RIGHT)

        if node.x > 0 and self.can_move_time(node.y, node.x - 1, time) and node.y >= 0:
            can.append(Wind.LEFT)


        if node.y > 0 and self.can_move_time(node.y -1, node.x, time):
            can.append(Wind.UP)

        if node.y < self.wy-1 and self.can_move_time(node.y +1, node.x, time):
            can.append(Wind.DOWN)

        if self.can_move_time(node.y, node.x, time) or node.y == -1:
            can.append(Wind.WAIT)

        return can

    def move(self, count = 1):
        while True:
            submoves = set()
            for nt in self.time_nodes[-1]:
                node = Node(nt[0], nt[1])
                ti = count
                moves = self.can_moves(node, count)

                for move in moves:
                    if move == Wind.DOWN:
                        submoves.add((node.x, node.y+1, ti))

                    elif move == Wind.RIGHT:
                        submoves.add((node.x+1, node.y,ti))

                    elif move == Wind.UP:
                        submoves.add((node.x, node.y-1, ti))

                    elif move == Wind.LEFT:
                        submoves.add((node.x-1, node.y,ti))

                    elif move == Wind.WAIT:
                        submoves.add((node.x, node.y,ti))

                    elif move == Wind.EXIT:
                        print("EXIT after moves: ", count)
                        sys.exit(0)
                    else:
                        assert False, "WTF"

            self.time_nodes[0] =submoves
            count += 1

    def run(self):
        count = 0
        count = self.move()
        print("Count:", count)

def test():
    global grid_loop
    lines = util.readlinesf('input')
    g = Grid(get_grid(lines))
    g.run()

test()

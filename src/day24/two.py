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
    __slots__ = ['grid', 'wx', 'wy', 'time_nodes', 'goalx']

    def __init__(self, grid, start='top'):
        self.grid = grid
        self.wx = len(self.grid[0])
        self.wy = len(self.grid)
        if start == 'top':
            self.time_nodes = [[(0, -1, 0)]]
            self.goalx = self.wx -1
        elif start == 'end':
            self.time_nodes = [[(self.wx-1, self.wy, 0)]]
            self.goalx = 0
        else:
            assert False, "WTF"

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

        if self.goalx == self.wx-1:
            if node.y == self.wy -1 and node.x == self.wx-1:
                can.append(Wind.EXIT)
                return can

        if self.goalx == 0:
            if node.y == 0 and node.x == 0:
                can.append(Wind.EXIT)
                return can


        if node.y < self.wy and node.y >= 0:
            if node.x < self.wx-1 and self.can_move_time(node.y, node.x + 1, time):
                can.append(Wind.RIGHT)

            if node.x > 0 and self.can_move_time(node.y, node.x - 1, time):
                can.append(Wind.LEFT)


        if node.y > 0 and self.can_move_time(node.y -1, node.x, time):
            can.append(Wind.UP)

        if node.y < self.wy-1 and self.can_move_time(node.y +1, node.x, time):
            can.append(Wind.DOWN)

        if node.y == -1 or node.y == self.wy or self.can_move_time(node.y, node.x, time):
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
                        return count
                    else:
                        assert False, "WTF"

            self.time_nodes[0] =submoves
            count += 1

    def run(self, count):
        count = self.move(count)
        print("Count:", count)
        return count

def test():
    global grid_loop
    lines = util.readlinesf('test_input')

    g = Grid(get_grid(lines), 'top')
    c=g.run(1)

    g = Grid(get_grid(lines), 'end')
    c=g.run(c+1)

    g = Grid(get_grid(lines), 'top')
    c=g.run(c+1)


test()

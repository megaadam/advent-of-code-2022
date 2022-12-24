import sys
sys.path.append('../util')
import util

from enum import Enum

# https://adventofcode.com/2022/day/24

lines = []
grid = []

Wind = Enum('Wind', ['UP', 'DOWN', 'LEFT', 'RIGHT'])

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
    __slots__ = ['grid', 'ex', 'ey', 'trail']

    def __init__(self, grid):
        self.grid = grid
        self.trail = []
        self.ex = 0
        self.ey = None

    def print(self):
        for gl in self.grid:
            for c in gl:
                if len(c) == 0:
                    print('.', end='')
                elif len(c) == 1:
                    print(cp(c), end='')
                else:
                    print(len(c), end='')
            print()

    def tick(self):
        ng = []
        for y, grid_line in enumerate(self.grid):
            ngl = []
            for x, cell in enumerate/grid_line:
                nc = self.from_four(x, y)
                ngl.append(nc)
            ng.append(ngl)

        self.grid = ng
        self.print()

def test():
    lines = util.readlinesf('test_input')
    g = Grid(get_grid(lines))
    g.print()
test()






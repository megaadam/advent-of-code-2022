import sys
sys.path.append('../util')
import util

import copy

from enum import Enum

# https://adventofcode.com/2022/day/24

lines = []
grid = []

Wind = Enum('Wind', ['UP', 'DOWN', 'LEFT', 'RIGHT', 'WAIT'])

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
    __slots__ = ['grid', 'x', 'y', 'trail']

    def __init__(self, grid):
        self.grid = grid
        self.trail = []
        self.x = 0
        self.y = -1

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

    def from_four(self, x,y):
        gl = len(self.grid[0])
        gh = len(self.grid)

        lx = (gl + x - 1) % gl # left from xy
        rx = (gl + x + 1) % gl # right from
        ay = (gh + y - 1) % gh # above
        by = (gh + y + 1) % gh # below

        res = set()
        if Wind.RIGHT in self.grid[y][lx]:
            res.add(Wind.RIGHT)

        if Wind.LEFT in self.grid[y][rx]:
            res.add(Wind.LEFT)

        if Wind.UP in self.grid[by][x]:
            res.add(Wind.UP)

        if Wind.DOWN in self.grid[ay][x]:
            res.add(Wind.DOWN)

        return res

    def tick(self):
        ng = []
        for y, grid_line in enumerate(self.grid):
            ngl = []
            for x, cell in enumerate(grid_line):
                nc = self.from_four(x, y)
                ngl.append(nc)
            ng.append(ngl)

        self.grid = ng

    def can_moves(self):
        can = set()
        if self.y == len(self.grid)-1 and self.x == len(self.grid[0]):
            set.add("EXIT")
            return

        if self.y < len(self.grid)-1 and len(self.grid[self.y+1][self.x]) == 0:
            can.add(Wind.DOWN)
            if self.y == -1:
                return can

        if self.x < len(self.grid[0])-1 and len(self.grid[self.y][self.x+1]) == 0:
            can.add(Wind.RIGHT)


        if self.x > 0 and len(self.grid[self.y][self.x-1]) == 0:
            can.add(Wind.LEFT)

        if self.y > 0 and len(self.grid[self.y-1][self.x]) == 0:
            can.add(Wind.UP)

        if len(self.grid[self.y][self.x]) == 0:
            can.add(Wind.WAIT)

        return can

    def move(self, count = 0, grid=None):

        grid = copy.deepcopy(self)

        moves = grid.can_moves()
        if 'EXIT' in moves:
            print("Done?")
            return count

        if count > 32:
            return count

        if len(moves) == 0:
            return 999999999

        counts = []

        for m in moves:
            if m == Wind.DOWN:
                grid.y += 1
                grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.RIGHT:
                grid.x += 1
                grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.UP:
                grid.y -= 1
                grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.LEFT:
                grid.x -= 1
                grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.WAIT:
                grid.tick()
                counts.append(grid.move(count+1))

            else:
                assert False, "WTF"

        return min(counts)

    def run(self):
        count = 0

        self.tick()
        self.print()
        self.move()
        count +=1
        print("Count:", count)

def test():
    lines = util.readlinesf('test_input')
    g = Grid(get_grid(lines))
    g.run()

test()






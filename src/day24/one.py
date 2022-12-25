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

MAXCOUNT = 995
mincount = MAXCOUNT

class TimeNode:
    __slots__ = ['x', 'y', 'time', 'moves']

    def __init__(self, x, y, time=0, moves=[]):
        self.x = x
        self.y = y
        self.time = time
        moves=moves



def grid_at_time(t):
    global grid_loop

    return grid_loop[t%len(grid_loop)]

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

def get_grid_loop(grid):
    xl = len(grid.grid[0])
    yl = len(grid.grid)
    ll = xl * yl

    print("get_grid_loop")
    grid_loop=[]
    for i in range(ll):
        g = copy.deepcopy(grid.grid)
        grid_loop.append(g)
        grid.tick()
        if i % 10 == 0:
            print('.', end='')
            sys.stdout.flush()





    print("GRIDLOOP done \n\n")
    return grid_loop

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
    __slots__ = ['grid', 'grid_static', 'x', 'y', 'wx', 'wy', 'time_nodes']

    def __init__(self, grid):
        self.grid = grid
        self.grid_static = copy.deepcopy(grid)
        self.x = 0
        self.y = -1
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


    def can_move_time(self, y, x, time):
        # Look right for left winds
        xr = (x + time) % self.wx
        if Wind.LEFT in self.grid_static[y][xr]:
            return False

        # Look left for right winds
        xl = (x - time) % self.wx
        if Wind.RIGHT in self.grid_static[y][xl]:
            return False

        # Look up for down winds
        yu = (y - time) % self.wy
        if Wind.DOWN in self.grid_static[yu][x]:
            return False

        # Look down ...
        yd = (y+time) % self.wy
        if Wind.UP in self.grid_static[yd][x]:
            return False

        return True


    def can_moves3(self, node, time):
        can = []

        if node.y == self.wy -1 and node.x == self.wx-1:
            can.append(Wind.EXIT)
            return can

        if node.x < self.wx-1 and self.can_move_time(node.y, node.x + 1, time):
            can.append(Wind.RIGHT)

        if node.x > 0 and self.can_move_time(node.y, node.x - 1, time):
            can.append(Wind.LEFT)


        if node.y > 0 and self.can_move_time(node.y -1, node.x, time):
            can.append(Wind.UP)

        if node.y < self.wy-1 and self.can_move_time(node.y +1, node.x, time):
            can.append(Wind.DOWN)

        if self.can_move_time(node.y, node.x, time) or node.y == -1:
            can.append(Wind.WAIT)

        return can


    def can_moves2(self, time):
        can = set()
        if self.y == len(self.grid_static)-1 and self.x == len(self.grid_static[0])-1:
            can.add(Wind.EXIT)
            return can

        if self.y < len(self.grid_static)-1 and self.can_move_time(self.y + 1, self.x, time):
            can.add(Wind.DOWN)
            if self.y == -1:
                return can

        if self.x < len(self.grid_static[0])-1 and self.can_move_time(self.y, self.x + 1, time):
            can.add(Wind.RIGHT)


        if self.x > 0 and self.can_move_time(self.y, self.x - 1, time):
            can.add(Wind.LEFT)

        if self.y > 0 and self.can_move_time(self.y - 1, self.x, time):
            can.add(Wind.UP)

        if self.can_move_time(self.y, self.x, time) or self.y == -1:
            can.add(Wind.WAIT)

        return sorted(list(can), key=lambda e:e.value)

    def can_moves(self):
        can = set()
        if self.y == len(self.grid)-1 and self.x == len(self.grid[0])-1:
            can.add(Wind.EXIT)
            return can

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

        if len(self.grid[self.y][self.x]) == 0 or self.y == -1:
            can.add(Wind.WAIT)

        return sorted(list(can), key=lambda e:e.value)



    def move2(self, count = 0):
        while True:
            submoves = set()
            for nt in self.time_nodes[-1]:
                node = TimeNode(nt[0], nt[1])
                ti = len(self.time_nodes)
                #print("======= self.time_nodes[-1][0].y", self.time_nodes[-1][0].y, "node", nxx.y)
                moves = self.can_moves3(node, len(self.time_nodes))

                for move in moves:
                    if move == Wind.DOWN:
                        # submoves.add(TimeNode(node.x, node.y +1))
                        submoves.add((node.x, node.y+1, ti))

                    elif move == Wind.RIGHT:
                        # submoves.add(TimeNode(node.x+1, node.y))
                        submoves.add((node.x+1, node.y,ti))

                    elif move == Wind.UP:
                        #submoves.add(TimeNode(node.x, node.y-1))
                        submoves.add((node.x, node.y-1, ti))

                    elif move == Wind.LEFT:
                        # submoves.add(TimeNode(node.x-1, node.y))
                        submoves.add((node.x-1, node.y,ti))

                    elif move == Wind.WAIT:
                        if len(self.time_nodes) == 0 or node.y > -1:
                            # submoves.add(TimeNode(node.x, node.y))
                            submoves.add((node.x, node.y,ti))

                    elif move == Wind.EXIT:
                        print("EXIT after moves: ", len(self.time_nodes))
                        sys.exit(0)
                    else:
                        assert False, "WTF"

            self.time_nodes.append(submoves)













    def move(self, count = 1):
        global mincount
        # self.grid = grid_at_time(count)

        moves = self.can_moves2(count)
        if Wind.EXIT in moves:
            mincount = min(mincount, count)
            return count

        if count > mincount:
            return mincount

        if len(moves) == 0:
            return MAXCOUNT

        counts = []

        for m in moves:
            grid = copy.deepcopy(self)
            if m == Wind.DOWN:
                grid.y += 1
                #grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.RIGHT:
                grid.x += 1
                #grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.UP:
                grid.y -= 1
                #grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.LEFT:
                grid.x -= 1
                #grid.tick()
                counts.append(grid.move(count+1))

            elif m == Wind.WAIT:
                #grid.tick()
                counts.append(grid.move(count+1))

            else:
                assert False, "WTF"

        return min(counts)

    def run(self):
        count = 0

        self.tick()
        count = self.move2()

        print("Count:", count)

def test():
    global grid_loop
    lines = util.readlinesf('test_input')
    g = Grid(get_grid(lines))

    # grid_loop = get_grid_loop(g)

    g.run()

test()

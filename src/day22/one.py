import sys
sys.path.append('../util')
import util

from enum import Enum
from dataclasses import dataclass

# https://adventofcode.com/2022/day/22

lines = []
grid = []
moves = []

Cell = Enum('Cell', ['NONE', 'OK', 'BLOCK'])

@dataclass
class Move:
    dx: int
    dy: int
    dist: int

dirval = {
    (1, 0):  0,
    (0, 1):  1,
    (-1, 0): 2,
    (0, -1): 3,
}

def turn_move(x, y, turn):
    right, left = turn == "R", turn == "L"

    if y == 0:
        y = x * right - x*left
        x = 0
    else:
        x = y * left - y*right
        y = 0

    return x, y

class Nav():
    __slots__ = ['x', 'y', 'dx', 'dy', 'move_len', 'grid']

    def __init__(self, grid):
        self.dx = 1
        self.dy = 0
        self.move_len = 0
        self.grid = grid

        for y, grid_line in enumerate(grid):
            for x, cell in enumerate(grid_line):
                if cell == Cell.OK:
                    self.x = x
                    self.y = y
                    return

        assert False, "WTF 1"

    def row_free(self):
        return not Cell.BLOCK in self.grid[self.y]

    def col_free(self, ymin, ymax):
        for y in range(ymin, ymax + 1):
            if self.grid[y][self.x] == Cell.BLOCK:
                return False

        return True

    def rowlen_minmax(self):
        xmin = min(self.grid[self.y].index(Cell.OK), self.grid[self.y].index(Cell.BLOCK))
        rev = self.grid[self.y][::-1]
        xmax = len(self.grid[self.y]) - min(rev.index(Cell.OK), rev.index(Cell.BLOCK)) -1

        return xmax - xmin +1, xmin, xmax

    def collen_minmax(self):
        x = self.x
        y = self.y

        while True:
            ymax = y
            y += 1
            if y > len(self.grid) -1 or self.grid[y][x] == Cell.NONE:
                break

        y = self.y
        while True:
            ymin = y
            y -= 1
            if y <0 or self.grid[y][x] == Cell.NONE:
                break

        return ymax - ymin + 1, ymin, ymax

    def run_move(self, move):
        if move.dy == 0:
            rowlen, xmin, xmax = self.rowlen_minmax()
            if self.row_free():
                d = move.dist % rowlen
            else:
                d = move.dist
        else:
            collen, ymin, ymax = self.collen_minmax()
            if self.col_free(ymin, ymax):
                d = move.dist % collen
            else:
                d = move.dist

        for _ in range(d):
                if move.dy == 0:
                    xtry = ((self.x + move.dx - xmin) % rowlen) + xmin
                    ytry = self.y
                else:
                    xtry = self.x
                    ytry = ((self.y + move.dy - ymin) % collen) + ymin

                if self.grid[ytry][xtry] == Cell.BLOCK:
                    break

                self.x = xtry
                self.y = ytry

    def run(self, moves):
        self.pgrid()
        for move in moves:
            # self.pmove(move)
            self.run_move(move)
            # self.pgrid()

        self.dx = moves[-1].dx
        self.dy = moves[-1].dy

    def final_password(self):
        p = 1000 * (self.y + 1) + 4 * (self.x + 1) + dirval[self.dx, self.dy]
        print("Final password: ", p)

    def pmove(self, move):
        dx = move.dx
        dy = move.dy

        for _ in range(4):
            if dy == 0:
                if dx==1:
                    print('>', end='')
                else:
                    print('<', end='')

            else:
                if dy == -1:
                    print('^', end='')
                else:
                    print('v', end='')

        print('  ', move.dist)

    def pgrid(self):
        for y in range(self.y + 3):
            for x, c in enumerate(self.grid[y]):
                #c = self.grid[y][x]
                if x == self.x and y == self.y:
                    print('*', end ='')
                elif c == Cell.NONE:
                    print(' ', end='')

                elif c == Cell.OK:
                    print('.', end='')

                elif c == Cell.BLOCK:
                    print('#', end='')

                else:
                    assert False, 'WTF'
            print()

        print()



def charcell(c):
    if c == ' ':
        return Cell.NONE
    if c == '.':
        return Cell.OK
    if c == '#':
        return Cell.BLOCK

    assert False, 'WTF'

def get_moves(moveline):
    num = ''
    moves = []
    dx = 1
    dy = 0
    for c in moveline:
        try:
            val = int(num + c)
            num += c
        except ValueError:
            turn = c
            moves.append(Move(dx, dy, val))
            dx, dy = turn_move(dx, dy, turn)
            num = ''
            val = 0

    moves.append(Move(dx, dy, val))

    return moves

def get_gridmoves(lines):
    lens = [len(l) for l in lines[:-2]]
    maxlen = max(lens)

    grid = []
    for line in lines[0:-2]:
        gridline = []
        for ix in range(maxlen):
            gridline.append(charcell(line[ix]) if ix < len(line) else Cell.NONE)
        grid.append(gridline)

    moves = get_moves(lines[-1])

    return grid, moves

def test():
    global grid, moves
    grid, moves = get_gridmoves(lines)
    m1 = get_moves('11L22L33L44LLL')
    m2 = get_moves('11R22R33R44RRR')

    nav = Nav(grid)
    nav.run(moves)
    nav.final_password()

lines = util.readlinesf_ns('input')

test()

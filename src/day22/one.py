import sys
sys.path.append('../util')
import util

from enum import Enum

# https://adventofcode.com/2022/day/22

lines = []
grid = []
moves = []

Cell = Enum('Cell', ['NONE', 'OK', 'BLOCK'])



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


class Nav():
    __slots__ = ['x', 'y', 'dx', 'dy', 'move_len']

    def __init__(self):
        self.dx = 1
        self.dy = 0
        self.move_len = 0

        for y, grid_line in enumerate(grid):
            for x, cell in enumerate(grid_line):
                if cell == Cell.OK:
                    self.x = x
                    self.y = y
                    return

        assert False, "WTF 1"


    def final_password1(self):
        p = 1000 * (self.y + 1) + 4 * (self.x + 1) + dirval(self.x, self.y)
        print("Final password: ", p)

    def run(self):
        for move in moves:
            if self.x:
                if self.row_free():
                    xm = self.x * (abs(move[0])) % self.rowlen()
                else:
                    xm = s
            self.apply_x(xm)




def charcell(c):
    if c == ' ':
        return Cell.NONE
    if c == '.':
        return Cell.OK
    if c == '#':
        return Cell.BLOCK

    assert False, 'WTF'

def get_moves(moveline):
    num = ""
    moves = []
    dx = 1
    dy = 0
    for m in moveline:
        try:
            val = int(num + m)
            num += m
        except ValueError:
            turn = m
            dx, dy = turnmove[dx, dy, turn]

    return moves

def get_gridmoves(lines):
    lens = [len(l) for l in lines]
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
    pass

lines = util.readlinesf_ns('test_input')

test()






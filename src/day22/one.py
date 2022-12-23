import sys
sys.path.append('../util')
import util

from enum import Enum

# https://adventofcode.com/2022/day/22

lines = []
grid = []

Cell = Enum('Cell', ['NONE', 'OK', 'BLOCK'])

L = "L"
R = "R"

class Nav():
    __slots__ = ['x', 'y', 'dx', 'dy']

    def __init__(self):
        self.dx = 1
        self.dy = 0

        for y, grid_line in enumerate(grid):
            for x, cell in enumerate(grid_line):
                if cell == Cell.OK:
                    self.x = x
                    self.y = y
                    return

        assert False, "WTF 1"


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
    for m in moveline:
        try:
            val = int(num + m)
            num += m
        except ValueError:
            move = (val, m)
            moves.append(move)
            num = ""

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
    global grid
    grid, moves = get_gridmoves(lines)
    pass

lines = util.readlinesf_ns('test_input')

test()






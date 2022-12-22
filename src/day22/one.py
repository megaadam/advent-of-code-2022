import sys
sys.path.append('../util')
import util

from enum import Enum

lines = []

Pos = Enum('Pos', ['NONE', 'OK', 'BLOCK'])

def charpos(c):
    if c == ' ':
        return Pos.NONE
    if c == '.':
        return Pos.OK
    if c == '#':
        return Pos.BLOCK

    assert False, 'WTF'

def get_gridmoves(lines):
    lens = [len(l) for l in lines]
    maxlen = max(lens)

    grid = []
    for line in lines[0:-2]:
        gridline = []
        for ix in range(maxlen):
            gridline.append(charpos(line[ix]) if ix < len(line) else Pos.NONE)
        grid.append(gridline)

    moves = lines[-1]

    return grid, moves


def test():
    grid, moves = get_gridmoves(lines)
    pass

lines = util.readlinesf_ns('test_input')

test()






import sys
sys.path.append('../util')
import util

import math

def get_grid(lines):
    grid = []
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))

        grid.append(row)
        
    return grid

def row(grid, r):
    return grid[r]

def col(grid, c):
    col = []
    for row in grid:
        col.append(row[c])
    return col

def columns(grid):
    # return the input rows of trees as columns of trees
    columns = []
    for line in grid:
        for ix, tree in enumerate(line):
            if len(columns) == ix:
                columns.append([])
            columns[ix].append(tree)

    return columns

def inside_count(grid):
    # count visible trees, INSIDE edge
    count = 0
    cols = columns(grid)
    for y, row in enumerate(grid[1:-1]):
        for x, tree in enumerate(row[1:-1]):
            if tree > max(row[:x+1]):  # visible from W ?
                count += 1
            elif tree > max(row[x+2:]): # visible from E ?
                count += 1
            elif tree > max(cols[x+1][:y+1]): # visible from N ?
                count += 1
            elif tree > max(cols[x+1][y+2:]): # visible from s ?
                count += 1

    return count

def edge_count(grid):
    return len(grid) * 2 + len(grid[0]) * 2 - 4

def test():
    lines = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
    ]

    grid = get_grid(lines)
    print("grid()", grid)

    print("row(3)", row(grid, 3))
    print("col(3)", col(grid, 3))
    print("edge_count()", edge_count(grid))
    print("columns(grid)", columns(grid))
    print("inside_count(grid)", inside_count(grid))

########################
# https://adventofcode.com/2022/day/8


test()

lines = util.readlines()
grid = get_grid(lines)
print(edge_count(grid) + inside_count(grid))
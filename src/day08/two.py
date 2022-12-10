import sys
sys.path.append('../util')
import util

import copy

def get_grid(lines):
    grid = []
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))

        grid.append(row)
        
    return grid

def columns(grid):
    # return the input rows of trees as columns of trees
    columns = []
    for line in grid:
        for ix, tree in enumerate(line):
            if len(columns) == ix:
                columns.append([])
            columns[ix].append(tree)

    return columns

def view_count(trees):
    # height: current height
    # trees: a list of trees in order of viewing, i.e. input order must be reveresed for North and East

    my_height = trees[0]
    for count, tree in enumerate(trees[1:]):
        if tree >= my_height:
            break

    return count + 1

def scenic_score(grid, cols, x, y):
    # scenic score for positio x,y
    # will fail for edge
    
    # count in east, east, south, north
    e = view_count(grid[y][x:])
    w = view_count(list(reversed(grid[y][:x+1])))
    s = view_count(cols[x][y:])
    n = view_count(list(reversed(cols[x][:y+1])))
    return w*e*s*n


def find_max_score(grid):
    cols = columns(grid)
    max_score = 1
    for y, row in enumerate(grid[1:-1]):
        for x, tree in enumerate(row[1:-1]):
            max_score = max(max_score, scenic_score(grid, cols, x+1, y+1))

    return max_score

def test():
    lines = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
    ]

    grid = get_grid(lines)
    cols = columns(grid)
    print("scenic_score #1", scenic_score(grid, cols, 2, 1))



    print("scenic_score #2", scenic_score(grid, cols, 2, 3))

    print("max_score", find_max_score(grid))

########################
# https://adventofcode.com/2022/day/8#part2


test()

lines = util.readlines()
grid = get_grid(lines)

print(find_max_score(grid))
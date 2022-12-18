import sys
sys.path.append('../util')
import util

import copy


raw_shapes = [
    ['####',],

    ['.#.',
     '###',
     '.#.',],

    ['..#',
     '..#',
     '###',],

    ['#',
     '#',
     '#',
     '#',],

    ['##',
     '##',],
]

def get_shapes():
    # convert raw_shapes to a 2D-matrix of bool

    shapes = []
    for raw_shape in raw_shapes:
        shape = []
        for raw_line in raw_shape:
            line = []
            for cell in raw_line:
                if cell == '#':
                    line.append(True)
                else:
                    line.append(False)
            
            shape.append(line)
        shapes.append(shape)
    
    return shapes

shapes = get_shapes()


ix = 0
def next_shape():
    global ix
    shape = shapes[ix % len(shapes)]
    ix+=1
    
    return shape

i2 = 0
def next_move():
    global i2

    if raw_moves[i2 % len(raw_moves)] == '<':
        i2 +=1
        return -1
    elif raw_moves[i2 % len(raw_moves)] == '>':
        i2+=1
        return +1

    else:
        assert False, "WTF"
    
    return 0


def get_line(width=7):
    return [False]*width

def init_pit(pit, shape = [], width=7, headroom=3):
    for _ in range(len(shape) + headroom):
        pit.insert(0, get_line())
    

def can_fall(pit, shape, shape_x, shape_y):
    if shape_y + len(shape) == len(pit):
        return False

    for iy, shape_line in enumerate(shape):
        for ix, cell in enumerate(shape_line):
            if cell and pit[shape_y+iy+1][shape_x+ix]:
                return False

    return True


def can_move(pit, shape, move, shape_x, shape_y):
    width = len(pit[0])
    if shape_x+move < 0 or shape_x+len(shape[0])+move>7:
        return False

    for iy, shape_line in enumerate(shape):
        for ix, cell in enumerate(shape_line):
            if cell and pit[shape_y+iy][shape_x+ix+move]:
                return False

    return True

def extend_pit(pit, shape, headroom=3, width=7):
    if len(pit) == 0:
        init_pit(pit, shape)
        return pit
    
    for iy,line in enumerate(pit):
        if sum(line):
            diff = (len(shape)-iy+headroom)
            if diff < 0:
                pit=pit[-diff:]
                return pit

            for _ in range(diff):
                pit.insert(0, get_line())
            return pit

def calc_height(pit):
    for iy,line in enumerate(pit):
        if sum(line):
            return len(pit) - iy

    return 0

def merge(pit, shape, shape_x, shape_y):

    for iy, shape_line in enumerate(shape):
        for ix, cell in enumerate(shape_line):
            if pit[shape_y+iy][shape_x+ix] and cell:
                assert False, "Merge WTF"
            if cell:
                pit[shape_y+iy][shape_x+ix] = cell

    
def print_pit(pit, shape=[], shape_y=0):
    print()
    for iy, line in enumerate(pit):
        for ix, pos in enumerate(line):
            if shape and shape_y == 0 and ix > 1 and ix-2<len(shape[0]) and iy<(len(shape)):
                if shape[iy][ix-2]:
                    print('@', end='')
                else:
                    print('.', end='')
            
                continue

            if pos:
                print('#', end='')
            else:
                print('.', end='')
        print()


def run_moves(target, wdith=7):

    pit = []
    shape = next_shape()
    init_pit(pit, shape)

    shape_x = 2
    shape_y = 0

    last_height=0

    big_fact = len(shapes) * len(raw_moves)

    def cyclical_loop(reps):
        nonlocal pit, shape, shape_x, shape_y
        old_height = calc_height(pit)
        for counter in range(reps):
            while(True):
                move = next_move()


                if(can_move(pit, shape, move, shape_x, shape_y)):
                    shape_x += move

                if can_fall(pit, shape, shape_x, shape_y):
                    shape_y += 1
                else:
                    # came to halt
                    # merge
                    merge(pit, shape, shape_x, shape_y)

                    # next
                    shape = next_shape()
                    shape_x = 2
                    shape_y = 0
                    pit = extend_pit(pit, shape)
                    # print_pit(pit, shape)
                    break
        
        return calc_height(pit), calc_height(pit) - old_height

    base_height, _ = cyclical_loop(big_fact)
    base_pit = copy.deepcopy(pit) # save this
    height_cycle = []
    while True:
        h, diff= cyclical_loop(big_fact)
        height_cycle.append(diff)
        if len(height_cycle) % 2 == 0:
            l2 = len(height_cycle) // 2
            if height_cycle[l2:] == height_cycle[:l2]:
                # height cycle now contains exactly two cycles
                break
    
    c_len = len(height_cycle)
    acc_height = base_height # before cycle
    cylcles_fit = (target - 1) // (c_len * big_fact)

    cycles_left = target - big_fact - cylcles_fit * len(height_cycle)
    c_height = sum(height_cycle)
    cycle_block_height = cylcles_fit * c_height

    pit = copy.deepcopy(base_pit)
    new_hight, _ = cyclical_loop(cycles_left)

    height = cycle_block_height + new_hight

    pass




                


        
        


    h = calc_height(pit)
    print("Height: ", h)



target = 2022

def test():
    print("raw moves", len(raw_moves))
    run_moves(target)



f = open('test_input', 'r')
#f = open('input', 'r')
lines = f.readlines()
raw_moves = lines[0].rstrip()
test()

print('ix', ix, 'i2',i2)

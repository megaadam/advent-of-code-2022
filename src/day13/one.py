import sys
sys.path.append('../util')
import util
import json

# https://adventofcode.com/2022/day/13

def comp(v1, v2):  # for comapring val as well as depth
    if v1 < v2:
        return -1
    if v1 == v2:
        return 0
    return 1

def compare_node(v1, d1, v2, d2):
    # return:  -1,  0, +1
    # for:      <, ==,  >

    if v1 == None and v2 == None:  # any None is end of node tree
        return 0
    if v1 == None:
        return True
    if v2 == None:
        return False

    if type(v1) == int and type(v2) == int:
        if v1 == v2:
            return comp(d1, d2)
        return comp(v1, v2)

    if type(v1) == list and type(v2) == list:  # only empty lists will reach this point
        return 0

    if type(v1) == list:
        return -1

    return 1  # v1 is int, v2 is []

def walk_generator(l, d=0):
    if type(l) == int:
        yield l, d

    else:
        assert type(l) == list
        if len(l) == 0:
            yield [], d

        for sub in l:
            yield from walk_generator(sub, d+1)

        yield [], d

def compare_walk(pair):
    # True  for <=
    # False for >
    w0 = walk_generator(pair[0])
    w1 = walk_generator(pair[1])

    while True:
        v1, d1 = next(w0, (None, None))
        v2, d2 = next(w1, (None, None))

        if v1 == None and v2 == None:
            return True

        if v1 == None:
            return True

        if v2 == None:
            return False

        c = compare_node(v1, d1, v2, d2)
        if c == 0:
            continue

        if c == -1:
            return True

        return False

def count_pairs(pairs, p=False):
    sum = 0

    for ix, pair in enumerate(pairs):
        if compare_walk(pair):
            if p:
                print("==", ix, "==")
            sum += ix + 1

    print("GRAND TOTAL:", sum)

def get_pairs(lines):
    pairs = []
    while lines:
        l_lines = lines.pop(0)
        r_lines = lines.pop(0)

        l = json.loads(l_lines)
        r = json.loads(r_lines)

        if len(lines) == 0:
            break # if no blank at end

        blank = lines.pop(0)
        assert blank == ""

        pairs.append((l,r))

    return pairs


count_pairs(get_pairs(util.readlinesf('test_input')))

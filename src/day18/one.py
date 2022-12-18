import sys
sys.path.append('../util')
import util

lines = []
blocks = set()
def get_blocks(lines=lines):
    global blocks
    for line in lines:
        raw_coords = line.split(',')

        cl = []
        for c in raw_coords:
            cl.append(int(c))

        block = (cl[0], cl[1], cl[2])
        assert block not in blocks, 'WTF!'
        blocks.add(block)
    

lines = util.readlinesf('test_input')

get_blocks(lines)

def test():
    pass

test()


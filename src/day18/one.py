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
    
def probe_set(s):
    p = (
         (s[0]+1, s[1], s[2]),
         (s[0]-1, s[1], s[2]),
         (s[0], s[1]+1, s[2]),
         (s[0], s[1]-1, s[2]),
         (s[0], s[1], s[2]+1),
         (s[0], s[1], s[2]-1),
    )
    return p

def get_surface():
    global blocks
    count = 0
    new=set()
    for c in blocks:
        p = probe_set(c)
        i = new.intersection(p)
        count += 6 - 2*len(i)
        new.add(c)
    
    return count


def test():
    global blocks

    blocks=set(((1,1,1), (1,2,1),(2,1,1)))
    print("Trivial surface:", get_surface()) # expect 14

test()

lines = util.readlinesf('test_input')
get_blocks(lines)
s = get_surface()

print('Surface: ', s)


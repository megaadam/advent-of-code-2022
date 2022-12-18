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

def get_surface(blocks, cavities=set()):
    my_blocks = blocks.copy()
    my_blocks.update(cavities)
    count = 0
    new=set()
    for c in my_blocks:
        p = probe_set(c)
        i = new.intersection(p)
        count += 6 - 2*len(i)
        new.add(c)
    
    print("Surface: ", count)
    return count

def get_surface2(blocks):
    blocks
    count = 0
    
    for c in blocks:
        p = probe_set(c)
        i = blocks.intersection(p)
        count += 6 - len(i)

    print("Surface #2: ", count)

    return count

def minmax(blocks):
    x = set([c[0] for c in blocks])
    y = set([c[1] for c in blocks])
    z = set([c[2] for c in blocks])

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    zmin = min(z)
    zmax = max(z)

    return xmin, xmax, ymin, ymax, zmin, zmax

    
def megablock(block):
    # return the cuboid surrounding (block)

    xmin, xmax, ymin, ymax, zmin, zmax = minmax(blocks)
    megablock = set()
    for x in range(xmin,xmax+1):
        for y in range(xmin,xmax+1):
            for z in range(zmin,zmax+1):
                c = (x,y,z)
                megablock.add(c)
    
    print(f"megablock: {xmax-xmin} x {ymax-ymin} x {zmax-zmin} volume: {(xmax-xmin) * (ymax-ymin) * (zmax-zmin)}")
    return megablock

def find_hollow():
    # Trivial 1-block-hollow only
 
    xmin, xmax, ymin, ymax, zmin, zmax = minmax(blocks)
    
    for x in range(xmin,xmax):
        for y in range(xmin,xmax):
            for z in range(zmin,zmax):
                c = (x,y,z)
                if c not in blocks:
                    i = blocks.intersection(probe_set(c))
                    if len(i) == 6:
                        print("hollow at: ", c)

def get_non_extertior(exterior, blocks):
    non_blocks = megablock(blocks).difference(blocks)
    # return set of non-exterior holes, i.e. cavities

    maybe_exterior = non_blocks.difference(exterior)

    def recurse():
        nonlocal maybe_exterior, exterior

        while exterior:
            c = exterior.pop()
            connected = maybe_exterior.intersection(probe_set(c))
            if connected:
                exterior.add(connected)
                maybe_exterior = maybe_exterior.difference(connected)
                recurse()
                
    recurse()
    return maybe_exterior
    pass

def get_exterior(blocks):
    # return non-exterior non-blocks
    non_blocks = megablock(blocks).difference(blocks)
    xmin, xmax, ymin, ymax, zmin, zmax = minmax(blocks)

    outmost = set() # all six "non-walls"

    for y in range (ymin, ymax+1):
        for z in range (zmin, zmax+1):
            if (xmin,y,z) in non_blocks:
                outmost.add((xmin,y,z))
                
    for y in range (ymin, ymax+1):
        for z in range (zmin, zmax+1):
            if (xmax,y,z) in non_blocks:
                outmost.add((xmax,y,z))
                
    for x in range (ymin, ymax+1):
        for z in range (zmin, zmax+1):
            if (x,ymin,z) in non_blocks:
                outmost.add((x,ymin,z))
                
    for x in range (ymin, ymax+1):
        for z in range (zmin, zmax+1):
            if (x,ymin,z) in non_blocks:
                outmost.add((x,ymax,z))
                
    for x in range (xmin, xmax+1):
        for y in range (ymin, ymax+1):
            if (x,y,zmin) in non_blocks:
                outmost.add((x,y,zmin))
                
    for x in range (xmin, xmax+1):
        for y in range (ymin, ymax+1):
            if (x,y,zmax) in non_blocks:
                outmost.add((x,y,zmax))
                
    # outmost now contains exterior walls
    return outmost
     




def test():
    global blocks

    get_surface(blocks)
    find_hollow()

    ext = get_exterior(blocks)
    non_ext = get_non_extertior(ext, blocks)
    get_surface(blocks)
    s= get_surface(blocks, non_ext)
    
    get_surface(blocks)
    get_surface2(blocks)


lines = util.readlinesf('input')
get_blocks(lines)
test()


import sys
sys.path.append('../util')
import util

def get_moves(lines):

    # a list of tupples 
    # eg [{"R", 4}, {"U", 4}]
    moves = []

    for line in lines:
        moves.append((line[0], int(line[2:])))

    return moves

class Knot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get(self):
        return (self.x, self.y)

class Engine:
    # It hardly matters but who knows
    __slots__ = ['trail', 'head', 'knots', 'minx', 'maxx', 'miny', 'maxy']

    def __init__(self):
        self.trail = set()
        self.knots = []
        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0
        for _ in range(0,10):
            self.knots.append(Knot(0, 0))

    def H(self):
        return self.knots[0]

    def knot_val(self, x,y):
        for i, knot in enumerate(self.knots):
            if x==self.knots[i].x and y==self.knots[i].y:
                if i==0:
                    return 'H'
                else:
                    return str(i)
        
        return '.'

    def minmax(self):
        # update minmax for trail render
        self.minx = min(self.minx, self.H().x)
        self.maxx = max(self.maxx, self.H().x)
        self.miny = min(self.miny, self.H().y)
        self.maxy = max(self.maxy, self.H().y)

    def tailtrail(self):
        self.trail.add(self.knots[len(self.knots)-1].get())

    def planck_ortho(self, pull):
        # True only if Planck distance is exceeded
        xdiff = abs(self.knots[pull].x - self.knots[pull-1].x) > 1
        ydiff = abs(self.knots[pull].y - self.knots[pull-1].y) > 1

        return xdiff != ydiff 

    def planck_diag(self, pull):
        xdiff = abs(self.knots[pull].x - self.knots[pull-1].x)
        ydiff = abs(self.knots[pull].y - self.knots[pull-1].y)

        return xdiff + ydiff > 2

    def run_moves(self, moves):
        for move in moves:
            for _ in range(move[1]):
                if move[0] == 'U':
                    self.knots[0].y += 1
                    self.minmax()
                    for i in range(1, len(self.knots)):
                        if self.planck_ortho(i):
                            self.knots[i].x = self.knots[i-1].x
                            self.knots[i].y += 1
                        elif self.planck_diag(i):
                            self.knots[i].y = self.knots[i-1].y
                        self.tailtrail()

                elif move[0] == 'D':
                    self.knots[0].y -= 1
                    self.minmax()
                    for i in range(1, len(self.knots)):
                        if self.planck_ortho(i):

                            self.knots[i].x = self.knots[i-1].x
                            self.knots[i].y -= 1
                            self.tailtrail()

                elif move[0] == 'L':
                    self.knots[0].x -= 1
                    self.minmax()
                    for i in range(1, len(self.knots)):
                        if self.planck_ortho(i):

                            self.knots[i].y = self.knots[i-1].y
                            self.knots[i].x -= 1
                            self.tailtrail()


                else:
                    self.knots[0].x += 1
                    self.minmax()
                    for i in range(1, len(self.knots)):
                        if self.planck_ortho(i):

                            self.knots[i].y = self.knots[i-1].y

                            self.knots[i].x += 1
                            self.tailtrail()
            self.render_moves()
            pass


    def render_moves(self):
        width = self.maxx - self.minx
        height = self.maxy - self.miny

        for y in reversed(range(height + 1)):
            for x in range(width+1):
                print(self.knot_val(x+self.minx, y+self.miny), end='')
            print()

        print('\n\n')
#def test_print_trail(engine):


def test():
    lines = [
    'R 5',
    'U 8',
    'L 8',
    'D 3',
    'R 17',
    'D 10',
    'L 25',
    'U 20',
    ]

    lines = [
    'R 4',
    'U 2', # U4
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2',
    ]


    moves = get_moves(lines)
    print(moves)

    engine = Engine()
    engine.run_moves(moves)

    print(list(sorted(list(engine.trail))))
    engine.render_moves()    
    print(len(engine.trail))
########################
# https://adventofcode.com/2022/day/9#part2

test()

#lines = util.readlines()
#moves = get_moves(lines)
#engine = Engine()
#engine.run_moves(moves)



#print(len(engine.trail))

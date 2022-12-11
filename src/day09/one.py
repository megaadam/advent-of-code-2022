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

class Engine:
    # It hardly matters but who knows
    __slots__ = ['trail', 'headx', 'heady', 'tailx', 'taily']

    def __init__(self):
        self.trail = set()
        self.headx = 0
        self.heady = 0
        self.tailx = 0
        self.taily = 0
        self.trail.add((self.tailx, self.taily))

    def planck_distance(self):
        # True only if Planck distance is exceeded
        return abs(self.headx-self.tailx) > 1 or abs(self.heady-self.taily) > 1

    def run_moves(self, moves):
        for move in moves:
            for _ in range(move[1]):
                if move[0] == 'U':
                    self.heady += 1
                    if self.planck_distance():
                        self.tailx = self.headx
                        self.taily = self.heady - 1
                        self.trail.add((self.tailx,self.taily))

                elif move[0] == 'D':
                    self.heady -= 1
                    if self.planck_distance():
                        self.tailx = self.headx
                        self.taily = self.heady + 1
                        self.trail.add((self.tailx,self.taily))

                elif move[0] == 'R':
                    self.headx += 1
                    if self.planck_distance():
                        self.tailx = self.headx - 1
                        self.taily = self.heady
                        self.trail.add((self.tailx,self.taily))

                else:
                    self.headx -= 1
                    if self.planck_distance():
                        self.tailx = self.headx + 1
                        self.taily = self.heady
                        self.trail.add((self.tailx,self.taily))


#def test_print_trail(engine):


def test():
    lines = [
    'R 4',
    'U 4',
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
    print(engine.trail)
    print(list(sorted(list(engine.trail))))
    print(len(engine.trail))
########################
# https://adventofcode.com/2022/day/9

test()

lines = util.readlines()
moves = get_moves(lines)
engine = Engine()
engine.run_moves(moves)

print(len(engine.trail))

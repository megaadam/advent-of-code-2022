import sys
sys.path.append('../util')
import util

monkeys = {}
class Monkey:
    __slots__ = ['name', 'op', 'pair_names', 'v1', 'v2', 'val']

    def __init__(self, name, op=None, v1=None, v2=None, val=None):
        self.name = name
        if v1 != None:
            self.pair_names = (v1, v2)
            self.op = op
            self.val = None
        else:
            self.val = int(val)
            self.pair_names = None
            self.op = None

        v1, v2 = None, None

    def eval(self):
        global monkeys
        if(self.val):
            return self.val

        else:
            v1 = monkeys[self.pair_names[0]]
            v2 = monkeys[self.pair_names[1]]

            if self.op == '+':
                return v1.eval() + v2.eval()

            if self.op == '-':
                return v1.eval() - v2.eval()

            if self.op == '*':
                return v1.eval() * v2.eval()

            if self.op == '/':
                return v1.eval() / v2.eval()

            print(self.name, self.v1, self.op, self.v2)
            assert False



def get_monkeys(lines):
    monkeys = {}

    for line in lines:
        halves = line.split(':')
        assert len(halves) == 2

        name = halves[0].strip()
        h2 = halves[1].strip()

        val, v1, v2 = None, None, None
        for op in ['+', '-', '*', '/']:
            if op in h2:
                vs = h2.split(op)
                assert len(halves) == 2

                v1 = vs[0].strip()
                v2 = vs[1].strip()
                break

        if v2 != None:
            monkey = Monkey(name, op, v1, v2)
        else:
            monkey = Monkey(name, val=h2)

        monkeys[name] = monkey

    return monkeys

def try_one_human(candidate):
    root = monkeys["root"]
    humn = monkeys["humn"]


    kid0 = monkeys[root.pair_names[0]]
    kid1 = monkeys[root.pair_names[1]]

    print(f"humn: {candidate}: ", end='')
    humn.val = candidate
    try:
        print(f"{kid0.eval()} <==> {kid1.eval()}")
        if kid0.eval() == kid1.eval():
            print("GOTCHA!")
            sys.exit(0)

    except Exception as e:
        print(e)

    return kid0.eval()

def try_humns(candidates):
    print('\n\n', candidates)

    # root = monkeys["root"]
    # humn = monkeys["humn"]

    # kid0 = monkeys[root.pair_names[0]]
    # kid1 = monkeys[root.pair_names[1]]


    for candidate in candidates:
        try_one_human(candidate)
        # print(f"humn: {candidate}: ", end='')
        # humn.val = candidate
        # try:
        #     print(f"{kid0.eval()} <==> {kid1.eval()}")
        #     if kid0.eval() == kid1.eval():
        #         print("GOTCHA!")
        #         sys.exit(0)

        # except Exception as e:
        #     print(e)


def bin_search(c1, c2):
    target = monkeys[monkeys["root"].pair_names[1]].eval()
    print("Target: ", target)
    print("Candidates", c1, c2)

    if c1 < c2:
        pos_dir = True
    else:
        pos_dir = False

    while (pos_dir and c1 < c2) or ((not pos_dir) and c2 < c1):
        cmid = (c1 + c2) / 2
        mid_val = try_one_human(cmid)  # will print and will exit on success
        if mid_val > target:
            c2 = cmid
        else:
            c1 = cmid

    assert False, "EXIT without found"

def test():

    root = monkeys["root"]


    # first tries
    try_humns([1,2,3,4,8,16])

    try_humns([-1024,-2048,-4096])

    # after several tries this is the (or one) candidate range
    try_humns([4096000000007])
    try_humns([2096000000007])




# https://adventofcode.com/2022/day/20

lines = util.readlinesf('input')

monkeys = get_monkeys(lines)

test()

bin_search(4096000000007, 2096000000007)

print(int(monkeys['root'].eval()))



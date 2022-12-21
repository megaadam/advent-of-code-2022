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




# https://adventofcode.com/2022/day/20

lines = util.readlinesf('input')

monkeys = get_monkeys(lines)
print(monkeys)

print(int(monkeys['root'].eval()))



import sys
sys.path.append('../util')
import util

class Monkey:
    __slots__ = ['name', 'op', 'pair_names', 'pair', 'val']

    def __init__(self, name, op=None, v1=None, v2=None, val=None):
        self.name = name
        if v1 != None:
            self.pair_names = (v1, v2)
            self.op = op
            self.val = None
        else:
            self.val = int(v1)
            self.pair_names = None
            self.op = None


def get_monkeys(lines):
    monkeys = {}

    for line in lines:
        halves = line.split(':')
        assert len(halves) == 2

        name = halves[0].rstrip()
        h2 = halves[1]

        val, v1, v2 = None, None, None
        for op in ['+', '-', '*', '/']:
            if op in h2:
                vs = h2.split(op)
                assert len(halves) == 2

                v1 = vs[0]
                v2 = vs[1]
                break


        if v2 != None:
            monkey = Monkey(name, op, v1, v2)
        else:
            monkey = Monkey(name, val=v1)

        monkeys[name] = name

    return monkeys





# https://adventofcode.com/2022/day/20

lines = util.readlinesf('test_input')

monkeys = get_monkeys(lines)
print(monkeys)



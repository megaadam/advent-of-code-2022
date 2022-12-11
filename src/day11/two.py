import sys
sys.path.append('../util')
import util

def extract(str, before, after):
    return(str[str.rfind(before)+len(before):str.find(after)])

def head_to(str, pat):
    return str[str.find(pat)]

def tail_from(str, pat):
    return str[str.rfind(pat)+len(pat):]

keys = ['op', 'true_monkey', 'false_monkey', 'exprs']

def items(tail):
    tokens = tail.split(', ')
    items= []
    for token in tokens:
        items.append(int(token))

    return items

class ExpressionList:
    __slots__ = ['exprs', 'cutoffs']

    def __init__(self):
        self.exprs = []
        # map of cutoff indexes keyed by divisor
        self.cutoffs = {}

def exprs(tail):
    tokens = tail.split(', ')
    exprs = []
    for token in tokens:
        el = ExpressionList()
        el.exprs = [int(token)]
        exprs.append(el)

    return exprs

MAXINDEX = 0

def divisible(expr, div):
    start = expr.cutoffs.get(div,1)
    if start == 1:
        val = expr.exprs[0]
    else:
        val = 0

    for i, op in enumerate(expr.exprs[start:]):
        if i > 187:
            # CRAZY stuff! magic number found through experimenting on tha actual data set
            return False
            
        if val % div == 0:
            expr.cutoffs[div] = i + start
            val = 0
        
        if op[0] == "+":
            val += op[1]
        elif op[0] == "*":
            val *= op[1]    
        else:
            val *= val
    
    return val % div == 0


def get_monkey_action(lines):
    monkeys = []

    for line in lines:
        if line.startswith('Monkey' ):
            monkey = {}
            monkey['count'] = 0
            num = int(extract(line, 'Monkey ', ':'))
            assert num == len(monkeys) # will need a dict if false

        elif ('Starting items: ') in line:
            monkey['exprs'] = exprs(tail_from(line, 'items: '))

        elif 'Operation: new = old ' in line:
            if 'old * old' in line:
                monkey['op'] = ('**', 0)  # square
                continue
            tail = tail_from(line, 'old ')
            op = tail[0]
            val = int(tail_from(tail, ' ')) 
            monkey['op'] = (op, val)

        elif 'Test: divisible by ' in line:
            monkey['divisor'] = int(tail_from(line, 'divisible by '))

        elif 'If true: throw to monkey ' in line:
            monkey['true_monkey'] = int(tail_from(line, 'monkey '))

        elif 'If false: throw to monkey ' in line:
            monkey['false_monkey'] = int(tail_from(line, 'monkey '))
            for key in keys:  # is this a good monkey ?
                assert key in monkey

            monkeys.append(monkey) 

    return monkeys

def run_monkey_action(monkeys):
    for monkey in monkeys:
        for expr in monkey['exprs']:
            # Op & Divisible & Throw
            expr.exprs.append(monkey['op'])

            if divisible(expr, monkey['divisor']):
                monkeys[monkey['true_monkey']]['exprs'].append(expr)

            else:
                monkeys[monkey['false_monkey']]['exprs'].append(expr)

            monkey['exprs'] = monkey['exprs'][1:]
            monkey['count'] += 1

def monkey_business(monkeys):
    counts = [monkey['count'] for monkey in monkeys if monkey['count'] > 0]
    top_monkeys = sorted(counts, reverse=True)
    return top_monkeys[0] * top_monkeys[1]

def test(external=False):
    lines = [
    'Monkey 0:',
    '  Starting items: 79, 98',
    '  Operation: new = old * 19',
    '  Test: divisible by 23',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 3',
    'Monkey 1:',
    '  Starting items: 54, 65, 75, 74',
    '  Operation: new = old + 6',
    '  Test: divisible by 19',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 0',
    'Monkey 2:',
    '  Starting items: 79, 60, 97',
    '  Operation: new = old * old',
    '  Test: divisible by 13',
    '    If true: throw to monkey 1',
    '    If false: throw to monkey 3',
    'Monkey 3:',
    '  Starting items: 74',
    '  Operation: new = old + 3',
    '  Test: divisible by 17',
    '    If true: throw to monkey 0',
    '    If false: throw to monkey 1',
    ]

    print(items(' 54, 65, 75, 74'))
    print(items('42'))
    if(external):
        lines = util.readlines()

    monkeys = get_monkey_action(lines)

    for i in range(10000):
        run_monkey_action(monkeys)
    print([m['count'] for m in monkeys])

    print('..................................')
    print(monkey_business(monkeys))

########################
# https://adventofcode.com/2022/day/9

test(True)

# lines = util.readlines()


import sys
sys.path.append('../util')
import util

def extract(str, before, after):
    return(str[str.rfind(before)+len(before):str.find(after)])

def head_to(str, pat):
    return str[str.find(pat)]

def tail_from(str, pat):
    return str[str.rfind(pat)+len(pat):]

keys = ['items', 'op', 'true_monkey', 'false_monkey']

def items(tail):
    tokens = tail.split(', ')
    items= []
    for token in tokens:
        items.append(int(token))

    return items

def get_monkey_action(lines):
    monkeys = []

    for line in lines:
        if line.startswith('Monkey' ):
            monkey = {}
            monkey["count"] = 0
            num = int(extract(line, 'Monkey ', ':'))
            assert num == len(monkeys) # will need a dict if false

        elif ('Starting items: ') in line:
            monkey['items'] = items(tail_from(line, 'items: '))

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
        for item in monkey['items']:
            # Operation
            if monkey["op"][0] == '*':
                item *= monkey["op"][1]
            elif monkey["op"][0] == '+':
                item += monkey["op"][1]
            else:
                item *= item

            # Bored
            item //= 3

            # Divisible & Throw
            if item % monkey['divisor'] == 0:
                monkeys[monkey['true_monkey']]["items"].append(item)
            else:
                monkeys[monkey['false_monkey']]["items"].append(item)

            monkey["items"] = monkey["items"][1:]
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
    print(monkeys)

    for _ in range(20):
        run_monkey_action(monkeys)

    print('..................................')

    print(monkeys)

    print('..................................')
    print(monkey_business(monkeys))

########################
# https://adventofcode.com/2022/day/9

test(True)

# lines = util.readlines()


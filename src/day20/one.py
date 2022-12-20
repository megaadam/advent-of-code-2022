import sys
sys.path.append('../util')
import util

class Node:
    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def append(self, node):
        self.next = node
        node.prev = self

class Circular:
    __slots__ = ['head', 'nodes', 'circlen']

    def __init__(self, lines):
        self.nodes = []  # will maintain original order

        self.circlen = len(lines)-1
        node = Node(int(lines[0]))
        self.nodes.append(node)
        self.head = node
        tail = node

        for line in lines[1:]:
            node = Node(int(line))
            self.nodes.append(node)

            tail.append(node)
            tail = node


        tail.next = self.head  # close the circular list
        self.head.prev = tail


    def move(self, node):
        insert_after = node

        if abs(node.val) % self.circlen == 0:
            return

        # convert steps to abs forward
        if node.val >= 0:
            steps = node.val % self.circlen
        else:
            steps = self.circlen - (abs(node.val) % self.circlen)


        for _ in range(steps):
            insert_after = insert_after.next

        # unlink
        node.prev.next = node.next
        node.next.prev = node.prev

        # insert "node" between "before" and "new_next"
        before = insert_after
        new_next = before.next

        # link backwards
        before.next = node
        node.prev = before

        # link forward
        new_next.prev = node
        node.next = new_next

    def run_moves(self):
        for node in self.nodes:
            self.move(node)

    def print(self, verbose=False, limit=20):
        print('Original:')
        for node in self.nodes[:min(limit, len(self.nodes))]:
            print(f'{node.val}, ', end='')

        if len(self.nodes) > limit:
            print('...')
        else:
            print()

        print('\nCircular list:')

        node = self.head
        for _ in range(min(limit, len(self.nodes))):
            print(f'{node.val}, ', end='')
            node = node.next

        if len(self.nodes) > limit:
            print('...')
        else:
            print()


        if verbose:
            for node in self.nodes[:min(limit, len(self.nodes))]:
                print(id(node))

        if len(self.nodes) > limit:
            print('...')
        else:
            print()


def test():
    vals =[-2,-1,0,20,1,3,7]

    circular = Circular(vals)
    circular.print()
    circular.run_moves()
    circular.print()

    vals = [1,2,3,4]
    circular = Circular(vals)
    circular.print()
    circular.run_moves()
    circular.print()


# https://adventofcode.com/2022/day/20
#test()

lines = util.readlinesf('test_input')
circular = Circular(lines)
circular.run_moves()
circular.print()



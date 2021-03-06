import copy
import functools
import helpers

import itertools
import collections


class Node:
    def __init__(self, n):
        self.val = n
        self.left = None
        self.right = None
        self.parent = None

    def render(self):
        if self.val is not None:
            return str(self.val)
        else:
            assert self.left.parent == self
            assert self.right.parent == self
            return f"[{self.left.render()}, {self.right.render()}]"

    def is_pair(self):
        return self.left and self.left.val is not None and self.right and self.right.val is not None

    def rightmost(self):
        n = self
        while n.right is not None:
            n = n.right
        return n

    def leftmost(self):
        n = self
        while n.left is not None:
            n = n.left
        return n

    def inorder(self, depth=0):
        if self.left:
            for n in self.left.inorder(depth+1):
                yield n
            yield self, depth
            for n in self.right.inorder(depth+1):
                yield n
        if self.val is not None:
            yield self, depth
    
def parse(f):
    n = Node(None)
    if type(f) is list:
        assert len(f) == 2
        n.left = parse(f[0])
        n.right = parse(f[1])
        n.left.parent = n
        n.right.parent = n
    else:
        n.val = f
    return n

def rightmost_add(n, val):
    prev = n
    n = n.parent
    while n.right == prev:
        prev = n
        n = n.parent
        if not n:
            return
        
    n = n.right.leftmost()
    if n.val is not None:
        n.val += val

def leftmost_add(n, val):
    prev = n
    n = n.parent
    while n.left == prev:
        prev = n
        n = n.parent
        if not n:
            return
        
    n = n.left.rightmost()
    if n.val is not None:
        n.val += val


def explode(f):
    for n, depth in f.inorder():
        if depth >= 4 and n.is_pair():
            left, right = n.left.val, n.right.val
            n.left = n.right = None
            n.val = 0
            rightmost_add(n, right)
            leftmost_add(n, left)
            return True
    return False

def split(n):
    ret = False
    for n, depth in n.inorder():
        if n.val is not None and n.val > 9:
#            print('split!', n.render())
            left = Node(n.val // 2)
            right = Node((n.val + 1) // 2)
            n.val = None
            n.left = left
            n.right = right
            left.parent = right.parent = n
            return True
    return False

def nice_explode(f, expected):
    e = parse(expected).render()
    print()
    n = parse(f)
    print(n.render())
    explode(n)
    print("got:", n.render())
    print("exp:", e)
    print(n.render() == e)

def nice_split(f, expected):
    e = parse(expected).render()
    print()
    n = parse(f)
    print(n.render())
    split(n)
    print("got:", n.render())
    print("exp:", e)
    print(n.render() == e)
    

def add(f1, f2):
    n = Node(None)
    n.left = f1
    f1.parent = n
    n.right = f2
    f2.parent = n

    return n

def chain(n):
#    print('chain!')
    acted = True
    while acted:
#        print('pre ', n.render())
        acted = explode(n)
        if not acted:
            acted = split(n)
#        print('post', n.render())

def magnitude(n):
    if n.val is not None:
        return n.val
    return 3 * magnitude(n.left) + 2 * magnitude(n.right)

def main() -> None:
    lines = helpers.read_input()
    fishes = []
    for f_str in lines:
        fishes.append(parse(eval(f_str)))

    for f1, f2 in itertools.permutations(fishes, 2):
        f1 = copy.deepcopy(f1)
        f2 = copy.deepcopy(f2)
        r = add(f1, f2)
        chain(r)
        print(magnitude(r))
         
main()

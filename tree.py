from pytz import timezone
import pytz

from atriact import *
from stuff import Incrementor

default_inc = Incrementor()

class Node:
    def __init__(self, data=(None, None, None, []), parent=None):

        self.parent = parent
        self.children = []
        self.I = Inh()
        self.S = Synth()
        self.index = default_inc.inc()
        (self.I.ptr, self.I.names, self.I.act, self.S.num) = data  # attributes

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return self

    def set_parent(self, parent):
        self.parent = parent
        return self

    def delete_child(self, index=None, sig=None):  # delete the state;
        if not index:
            if not sig:
                self.children.__delitem__(-1)
            else:
                pass
        else:
            for i,o in enumerate(self.children):
                if o.index == index:
                    del self.children[i]
        return self.children



    # search routines

    # recursive dfs
    def dfs(self, action=action_check_attr, **kwargs):
        current = self
        chk, current = action(current, **kwargs)
        if chk:
            return (chk, current)

        if len(current.children) <= 0:
            return (chk, current)
        else:
            if '__noprint__prefix' in kwargs:
                kwargs['__noprint__prefix'] += '|- '
            for node in current.children:
                try:
                    (chk, crnt) = node.dfs(action, **kwargs)
                except Exception as e:
                    print(e,'\n')
                if chk:
                    return chk, crnt  # ret from recursion

    # upward branch checking from current node to some global root

    def upbranch(self, action=action_check_attr, **kwargs):
        chk, current = False, self
        while current.parent != None:
            chk, current = action(current, **kwargs)
            if chk:
                break
            current = current.parent
        return chk, current


class Tree:  # represents a tree/subtree
    def __init__(self, root=Node()):
        self.root = root

    # recursive dfs
    def dfs(self, root=None, action=None, **kwargs):
        if not root:
            root = self.root
        current = root
        chk, current = action(current, **kwargs)
        if chk:
            return (chk, current)

        if len(current.children) == 0:
            return (chk, current)
        else:
            for node in current.children:
                (chk, crnt) = self.dfs(node)
                if chk:
                    return (chk, crnt)

    # upward branch checking from current root to some global root

    def upbranch(self, bottom=None, action=None, **kwargs):
        chk, current = False, self.root
        if bottom:  # метод умеет стартовать с некоторой выбранной вершины, не обязательно с корня (под)дерева
            current = bottom
        while current.parent != None:
            chk, current = action(current, **kwargs)
            current = current.parent
        return


def unittest():
    dummy = [1, 2, 3, 4, [], [], [], []]
    dummy2 = [5, 6, 7, 8, [], [], [], []]
    dummy3 = [9, 10, 11, 12, [], [], [], []]
    t = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))
    t.add_child(Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy2)))
    t.add_child(Node(data=(None, {'p': 0,
                                  'g': 1,
                                  's': 2,
                                  'pp': 3,
                                  'socket': 4,
                                  'pipe': 5,
                                  'fifo': 6,
                                  'files': 7}, None, dummy3)))
    print(t.S.num)
    print(t.children[1].S.num)
    print(id(t.children), id(t.children[1].children))

if __name__ == '__main__':
    unittest()
from pstree import *
from tree import *
from atriact import *
import pickle


def print_tree(root):
    root.dfs(action_print, __noprint__prefix='|- ', mode='parsed', p='p', g='g',s='s')


class Parser:
    def __init__(self, from_snapshot=False, in_mem=None, pkl_fn=None):
        if not from_snapshot:
            self.pstree = get_pstree()
        elif in_mem:
            self.pstree = in_mem
        else:
            try:
                self.pstree = pickle.load(pkl_fn)
            except Exception as e:
                print('Snapshot file loading error. System is forced to get snapshot of current state')
                self.pstree = get_pstree()

    def load_from_snapshot(self, in_mem=None, pkl_fn=None):
        if in_mem:
            self.pstree = in_mem
        else:
            try:
                self.pstree = pickle.load(pkl_fn)
            except Exception as e:
                print('Snapshot file loading error:', e)

    def update_pstree(self):
        self.pstree = get_pstree()

    def downward(self, print_res=False):
        if print_res:
            self.pstree.dfs(action_print, __noprint__prefix='|- ', mode='start', p='p', g='g', s='s')
        print('---------------------------Start parsing---------------------------------')
        self.pstree.dfs(action_reconstruct)
#        self.print_tree(self.pstree)
        print('-------------------------------Parsed. Printing results:------------------------------------------------')
        if print_res:
            self.pstree.dfs(action_print, __noprint__prefix='|- ', mode='parsed', p='p', g='g',s='s')


    def upward(self):
        # now no need upward because of tree hierarchy and attributes checking on tree construction
        pass

def exittest(mode='mem', number=1):
    if mode == 'mem':
        dummy = [0, 0, 0, 0, [], [], [], []]
        node_0 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [1, 1, 1, 0, [], [], [], []]
        node_1 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [2, 3, 5, 1, [], [], [], []]
        node_2 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [3, 1, 1, 2, [], [], [], []]
        node_3 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [4, 4, 1, 1, [], [], [], []]
        node_4 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [5, 1, 1, 4, [], [], [], []]
        node_5 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [6, 6, 6, 1, [], [], [], []]
        node_6 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [7, 4, 1, 4, [], [], [], []]
        node_7 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
#        node_1.add_child(node_4)

        node_1.add_child(node_2)
        '''
        node_1.add_child(node_6)
        node_4.add_child(node_5)
        node_2.add_child(node_3)
        node_6.add_child(node_7)
        '''
        node_0.add_child(node_1)

        p = Parser(from_snapshot=True, in_mem=node_1)

        p.downward(True)


def stubtest(mode='mem'):
    if mode == 'mem':
        if mode == 'mem':
            dummy = [0, 0, 0, 0, [], [], [], []]
            node_0 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))
            dummy = [1, 1, 1, 0, [], [], [], []]
            node_1 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))
            dummy = [2, 2, 2, 1, [], [], [], []]
            node_2 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))
            dummy = [3, 1, 1, 2, [], [], [], []]
            node_3 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            dummy = [4, 4, 4, 3, [], [], [], []]
            node_4 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            dummy = [5, 5, 5, 4, [], [], [], []]
            node_5 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            dummy = [6, 2, 2, 5, [], [], [], []]
            node_6 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            dummy = [7, 1, 1, 4, [], [], [], []]
            node_7 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            dummy = [8, 8, 8, 1, [], [], [], []]
            node_8 = Node(data=(None, {'p': 0,
                                       'g': 1,
                                       's': 2,
                                       'pp': 3,
                                       'socket': 4,
                                       'pipe': 5,
                                       'fifo': 6,
                                       'files': 7}, None, dummy))

            node_1.add_child(node_2)
            node_2.add_child(node_3)

            node_1.add_child(node_4)

            node_2.add_child(node_5)
            node_4.add_child(node_7)
            node_5.add_child(node_6)
            node_0.add_child(node_1)
            node_1.add_child(node_8)
            p = Parser(from_snapshot=True, in_mem=node_1)

            p.downward(True)

def unittest(mode='mem'):
    if mode == 'mem':
        dummy = [0, 0, 0, 0, [], [], [], []]
        node_0 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [1, 1, 1, 0, [], [], [], []]
        node_1 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [2, 2, 2, 1, [], [], [], []]
        node_2 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        dummy = [3, 1, 1, 2, [], [], [], []]
        node_3 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [4, 4, 1, 1, [], [], [], []]
        node_4 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [5, 1, 1, 4, [], [], [], []]
        node_5 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [6, 6, 6, 1, [], [], [], []]
        node_6 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))

        dummy = [7, 4, 1, 4, [], [], [], []]
        node_7 = Node(data=(None, {'p': 0,
                                   'g': 1,
                                   's': 2,
                                   'pp': 3,
                                   'socket': 4,
                                   'pipe': 5,
                                   'fifo': 6,
                                   'files': 7}, None, dummy))
        node_1.add_child(node_4)
        node_1.add_child(node_2)
        node_1.add_child(node_6)
        node_4.add_child(node_5)
        node_2.add_child(node_3)
        node_6.add_child(node_7)

        node_0.add_child(node_1)

        p = Parser(from_snapshot=True, in_mem=node_1)

        p.downward(True)


if __name__ == '__main__':
    exittest(mode='mem', number=2)

# tests:
# 0) 111[211] - passed
# 1) 111[222[311]] -> 111[fork211[setsid222,fork311]] - under debug
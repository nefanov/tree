from pstree import *
from tree import *
from atriact import *
import pickle


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
        self.pstree.dfs(action_reconstruct)
        print('Parsed. Printing results:')
        if print_res:
            self.pstree.dfs(action_print, __noprint__prefix='|- ', mode='parsed', p='p', g='g',s='s')
        pass

    def upward(self):
        # now no need upward because of tree hierarchy and attributes checking on tree construction
        pass


def unittest(mode='mem'):
    if mode == 'mem':
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
        node_1.add_child(node_2)
        node_2.add_child(node_3)
        p = Parser(from_snapshot=True, in_mem=node_1)

        p.downward(True)


if __name__ == '__main__':
    unittest(mode='mem')

# tests:
# 0) 111[211] - passed
# 1) 111[222[311]] -> 111[fork211[setsid222,fork311]] - under debug
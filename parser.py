from pstree import *
from tree import *
from atriact import *
import pickle
from stuff import normalize_str
from linear import *


def print_tree(root):
    root.dfs(action_print, __noprint__prefix='|- ', mode='parsed', p='p', g='g', s='s')


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


class LinearParser(Parser):
    import sortedcontainers

    def __init__(self, s, ord_list=sortedcontainers.SortedDict()):
        self.s = s
        self.arglist = ['p', 'g', 's', 'pp']
        self.idx = ord_list

    def add_string(self, s):
        self.s = s

    def lr_pass(self, s, root):
        self.pstree = self.first_stage(normalize_str(s), root=root)
        return self.pstree

    def first_stage(self, raw_line, stack=Stack(), dbg=False, root=None):
        current = root
        last_viewed = root
#        raw_line = normalize_str(raw_line)
        line = raw_line.split(' ')
        line = [x for x in line if x != '']
        pos = 0
        stack.push(['<s>'])  # root metadata

        while pos in range(len(line)):
            if line[pos] == '':
                pos+=1
                continue
            if (line[pos]).isdigit():
                cand = []
                for i in line[pos:pos + len(self.arglist)]:
                    if not (i).isdigit():
                        break
                    else:
                        cand.append(int(i))

                if len(cand) == len(self.arglist):
                    stack.push([proc(cand[0], cand[1], cand[2], cand[3])])  # automate it
                    self.idx[cand[0]] = [stack.sp - 1, 0]
                    # node stuff

                    new_state = Node(data=(None, default_inh, None, [cand[0],
                                                                     cand[1],
                                                                     cand[2],
                                                                     cand[3],
                                                                     [], [], [],
                                                                     []]))
                    last_viewed = new_state
                    last_viewed.parent = current

                    if cand[0] == 1:
                        current.add_child(new_state)

                    elif new_state.S[0] == new_state.S[1] and new_state.S[1] == new_state.S[2]:
                        new_state.I.act = 'setsid()'
                        new_state.visited = True
                        new_state_hidden = Node(data=(None, default_inh, None, [cand[0],
                                                                         current.S[1],
                                                                         current.S[2],
                                                                         cand[3],
                                                                         [], [], [],
                                                                         []]))
                        new_state_hidden.add_child(new_state)
                        current.add_child(new_state_hidden)

                    elif new_state.S[0] == new_state.S[1] and new_state.S[2] == current.S[2]:
                        new_state.I.act = 'setpgid(self)'
                        new_state.visited = True
                        new_state_hidden = Node(data=(None, default_inh, None, [cand[0],
                                                                                current.S[1],
                                                                                current.S[2],
                                                                                cand[3],
                                                                                [], [], [],
                                                                                []]))
                        new_state_hidden.add_child(new_state)
                        current.add_child(new_state_hidden)
                    elif new_state.S[2] == current.S[2] and new_state.S[1] == current.S[1]:
                        new_state.I.act = 'fork('+str(current.S[0])+')'
                        current.add_child(new_state)
                    else:
                        current.add_child(new_state)

                    if dbg == True:
                        print(stack[stack.sp - 1])
                    pos += len(self.arglist)
                    metadata = stack.frame_get_metadata()
                    metadata.append({stack.sp - 1: cand[0]})
                    stack.frame_update_metadata(metadata)
                else:
                    print("Parsing.error")
                    if dbg == True:
                        stack.print_stack()
                        print('Candidate', cand)

                        print("Position ", pos, line[pos], "in data ", line)
                    sys.exit(1)
            if line[pos] == '[':
                current = last_viewed
                stack.frame()
                stack.push([])
                pos += 1

            if line[pos] == ']':
                current = current.parent
                # parse, then unwind
                # implicit left-to-right rules match: setsid, setpgid(self), fork
                #				for rule in cf_rules:
                #					pass
                stack.unwind()
                pos += 1

        if dbg == True:
            print("==============================\n\n1st stage is finished. Stack is:")
            stack.print_stack()
        return root

def lineartest(s='1 1 1 0 [ 2 1  1   1  [  3  1 1 2 [  ]   ] 4 4 4 1 [  ]   ]'):
    print('Go')
    lp = LinearParser('')
#    lp.add_string(s)
    dummy = [0, 0, 0, 0, [], [], [], []]
    node_0 = Node(data=(None, {'p': 0,
                               'g': 1,
                               's': 2,
                               'pp': 3,
                               'socket': 4,
                               'pipe': 5,
                               'fifo': 6,
                               'files': 7}, None, dummy))
    res = lp.lr_pass(s, root=node_0)
    print('return from')
    return res





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
    l = lineartest()#(mode='mem')#, number=2)
    print('done')

# tests:
# 0) 111[211] - passed
# 1) 111[222[311]] -> 111[fork211[setsid222,fork311]] - under debug
# 'atriact': actions with attributes
default_inh={'p': 0,
            'g': 1,
            's': 2,
            'pp': 3,
            'socket': 4,
            'pipe': 5,
            'fifo': 6,
            'files': 7}
class Inh:
    def __init__(self, ptrs=None, names=None, act=None):
        self.ptr = ptrs
        self.names = names
        self.act = act

    def __str__(self):
        print('Node inherited attributes')
        print('lists:')
        try:
            print(self.ptr)
        except:
            print('No lists')
        try:
            print(self.names)
        except:
            print('No variables names')
        try:
            print(self.act)
        except:
            print('No syscall recognised')


class Synth:
    def __init__(self, values=[]):
        self.num = values

    def __getitem__(self, key):
        return self.num[key]

    def __setitem__(self, key, value):
        self.num[key] = value

    def __str__(self):
        print(self.num)


def check_cf(current, **kwargs):
    from tree import Node
    if not current.parent: # maybe Init process
        return False, current

    # 2 1 1
    if current.S[current.I.names['g']] == current.parent.S[current.parent.I.names['g']] and \
        current.S[current.I.names['s']] == current.parent.S[current.parent.I.names['s']]:
        current.I.act = 'fork' + '(' + str(current.S[current.I.names['pp']]) + ')'
        if 'check_fds' in kwargs:
            pass
    # 1 1 1
    elif current.S[current.I.names['p']] == current.S[current.I.names['g']] == current.S[current.I.names['s']]:
        new_state = Node(data=(None, default_inh, None, [current.S[current.I.names['p']],
                                    current.parent.S[current.parent.I.names['g']],
                                    current.parent.S[current.parent.I.names['s']],
                                    current.S[current.I.names['pp']],
                                    current.S[4], current.S[5], current.S[6], current.S[7]]), parent=current.parent)
        current.parent = new_state
        new_state.I.act = 'fork'+'('+str(new_state.S[new_state.I.names['pp']])+')'
        current.I.act = 'setsid()'
        new_state.add_child(current)
    # 1 2 1
    elif current.S[current.I.names['p']] == current.S[current.I.names['g']] != current.S[current.I.names['s']]:
        new_state = Node(data=(None, default_inh, None, [current.S[current.I.names['p']],
                                    current.parent.S[current.parent.I.names['g']],
                                    current.parent.S[current.parent.I.names['s']],
                                    current.S[current.I.names['pp']],
                                    current.S[4], current.S[5], current.S[6], current.S[7]]), parent=current.parent)
        current.parent = new_state
        new_state.I.act = 'fork'+'('+str(new_state.S[new_state.I.names['pp']])+')'
        current.I.act = 'setpgid'+'('+str(new_state.S[new_state.I.names['p']])+')'
        new_state.add_child(current)

        # check cs:
    elif current.parent.I.act == 'setsid()':##session_picker
        res, _ = current.upbranch(action=action_check_attr_eq, name='p', val=current.S[current.I.names['s']])
        if res:
            current.parent.children = current.parent.delete_child(current.index)
            current.parent = current.parent.parent
            current.parent.add_child(current)
            if current.S[current.I.names['g']] != current.parent.S[current.parent.I.names['g']]: ##loc_group(noself)
                resg, root = current.upbranch(action=action_check_attr_eq, name='p', val=current.S[current.I.names['s']])
                if resg:
                    r, _ = root.dfs(action=action_check_attr_eq, name='p', name2='g', val=current.S[current.I.names['g']])
                    if r:
                        new_state = Node(data=(None, default_inh, None, [current.S[current.I.names['p']],
                                                                         current.parent.S[current.parent.I.names['g']],
                                                                         current.parent.S[current.parent.I.names['s']],
                                                                         current.S[current.I.names['pp']],
                                                                         current.S[4], current.S[5], current.S[6],
                                                                         current.S[7]]), parent=current.parent)
                        current.parent = new_state
                        new_state.I.act = 'fork' + '(' + str(new_state.S[new_state.I.names['pp']]) + ')'
                        current.I.act = 'setpgid' + '(' + str(new_state.S[new_state.I.names['p']]) + ')'
                        new_state.add_child(current)

    return False, current


# action fmt: get attrs from tree, return True if cond, else false

def action_check_attr(current, **kwargs):
    if current.S[kwargs.pop('name')] == kwargs.pop('value'):
        return True, current
    return False, current


def action_check_attr_eq(current, **kwargs):
    val = kwargs.pop('val')
    for _, v in kwargs.items():
        if current.S[current.I.names[v]] != val:
            return False, current
    return True, current


def action_print(current, **kwargs):
    prefix = kwargs.pop('__noprint__prefix')
    for k, v in kwargs.items():
        if not '__noprint__' in k:
            print(prefix, current.S.num, current.S[current.I.names[v]])
    return False, current

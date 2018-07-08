from tree import *
import os
import sys
import pprint
from stuff import *

class Stack:
    def __init__(self):
        self.bp = 0
        self.sp = 0
        self.lr = 0  # for return pos - ARM link register analogue;)
        self.data = list()

    # In usage, the stack is represented as indexed structure,  from 0 to len-1:
    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, k, v):
        self.data[k] = v

    # Neverteless, FILO methods is also presented:
    def push(self, v):
        self.data.append(v)
        self.sp += 1  # STRIA - manner

    def pop(self):
        self.sp -= 1  # LDRDB - manner
        return self.data.pop()

    # stackframe routines is constructed like in ARM processors:
    # save the bp into lr and set bp = sp
    def frame(self):
        self.lr = self.bp
        self.bp = self.sp

    def unwind(self):
        self.bp = self.lr

    # metadata is on the first position of the frame
    def frame_update_metadata(self, v):
        try:
            self[self.bp] = v
        except:
            self.push(v)

    def frame_get_metadata(self):
        try:
            return self[self.bp]
        except:
            return []

    def print_stack(self):
        for i, idx in enumerate(self.data):
            print('[' + str(i) + ']:', idx)


# test
def test():
    s = stack()
    s.push(1)
    s.push(2)
    print(s.pop())


# This class describes single node in the IR tree
class proc:
    def __init__(self, p, g, s, pp, call='fork'):
        self.p = p
        self.g = g
        self.s = s
        self.pp = pp
        self.call = call

    def getpid(self):
        return self.p

    def getpgid(self):
        return self.g

    def getsid(self):
        return self.s

    def getppid(self):
        return self.pp

    def getcall(self):
        return self.call

    def setpid(self, p=1):
        self.p = p

    def setpgid(self, g=1):
        self.g = g

    def setsid(self, s=1):
        self.s = s

    def setppid(self, pp=1):
        self.pp = pp

    def setcall(self, call='fork'):
        self.call = call
# test frame

# s=stack()
# s.push(1)
# s.frame()
# s.frame_update_metadata('azaza')
# print(s[0],s[1])

# print(s.frame_get_metadata()) # expect 2
# s.push(5)
# print(s.pop())
# print(s.pop())


from enum import Enum


class Incrementor:
    def __init__(self, state=0):
        self.state = state

    def inc(self, step=1):
        self.state += step
        return self.state


class FileMode(Enum):
    ORDONLY = 0,
    OWRONLY = 1,
    ORDWR = 2,
    O_CLONEXEC = 0,
    O_CREAT = 400,
    O_EXCL = 2000,
    O_TRUNC = 1000,
    O_APPEND = 10,
    O_SYNC = 20



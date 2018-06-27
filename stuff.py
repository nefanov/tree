from enum import Enum


class FileMode(Enum):
    ORDONLY = 0,
    OWRONLY = 1,
    ORDWR = 2,
    O_CLONEXEC = 0,
    O_CREAT = 400,
    O_EXCL = 2000,
    O_TRUNC = 1000
    O_APPEND = 10,
    O_SYNC = 20



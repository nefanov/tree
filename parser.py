from pstree import *
from tree import *
from atriact import *
import pickle

class Parser:
    def __init__(self, pkl_fn):
        if not pkl_fn:
            self.pstree = get_pstree()
        else:
            try:
                self.pstree=pickle.load(pkl_fn)
            except Exception as e:
                print('Snapshot file loading error. System is forced to get snapshot of current state')
                self.pstree = get_pstree()

    def load_from_snapshot(self, pkl_fn):
        try:
            self.pstree=pickle.load(pkl_fn)
        except Exception as e:
            print('Snapshot file loading error.')



    def update_pstree(self):
        self.pstree = get_pstree()

    def downward(self):
        pass

    def upward(self):
        pass
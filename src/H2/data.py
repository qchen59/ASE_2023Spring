from utils import csv, map
from row import Row
from col import Col
from lists import kap


class Data:
    def __init__(self, src) -> None:
        self.rows = []
        self.cols = None
        if type(src) == str:
            csv(src)
        else:
            map(src)

    def add(self, t):
        if self.cols:                       # if column names have been seen
            t = t.cells and t or Row(t)     # ensure t is a row
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Col(t)

    def clone():
        # TODO: Did not understand. Will need the entire code to understand.
        pass

    def stats(self, what, cols, nPlaces):
        def fun(k, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()
            return col.rnd(val, nPlaces), col.txt
        return kap(cols or self.cols.y, fun)

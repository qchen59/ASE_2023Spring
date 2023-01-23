from utils import csv
from row import Row
from col import Col
from lists import Lists



class Data:
    def __init__(self, src) -> None:
        self.rows = []
        self.cols = None
        self.l = Lists()

        def helper(x):
            self.add(x)

        if type(src) == str:
            csv(src, helper)
        else:
            self.l.map(src, helper)

    def add(self, t):
        if self.cols:  # if column names have been seen
            t = Row(t)  # ensure t is a row
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Col(t)

    def clone(self):
        # TODO: Did not understand. Will need the entire code to understand.
        pass

    def stats(self, what, cols, nPlaces):
        def fun(k, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()

            return col.rnd(val, nPlaces), col.txt
        return self.l.kap(cols or self.cols.y, fun)

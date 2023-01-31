from utils import csv
from row import Row
from col import Col
from lists import Lists
from numerics import Numerics



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

    def half(i, rows=None, cols=None, above=None):
        
        # imports from other functions
        numerics = Numerics()
        lists = Lists()

        def project(row):
            return {'row': row, 'dist': numerics.cosine(dist(row, A), dist(row, B), c)}
        
        def dist(row1, row2):
            return i.dist(row1, row2, cols)
    
        rows = rows or i.rows
        some = numerics.many(rows, the.Sample)
        A = above or any(some)
        B = i.around(A, some)[int((the.Far * len(rows)) // 1)].row
        c = dist(A, B)
        left, right = [], []
        for n, tmp in enumerate(lists.sort(map(project, rows), key=lambda x: x['dist'])): # No idea if this is how it works
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        
        return left, right, A, B, mid, c

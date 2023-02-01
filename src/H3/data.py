import config
import math
from utils import csv
from row import Row
from col import Col
from lists import Lists
import config
import math
from numerics import Numerics


class Data:
    def __init__(self, src) -> None:
        self.rows = []
        self.cols = None
        self.l = Lists()
        self.nu = Numerics()

        def helper(x):
            self.add(x)
            # return None, None

        if type(src) == str:
            csv(src, helper)
        else:
            self.l.map(src, helper)

    def __repr__(self):
        return str(self.__dict__)

    def add(self, t):
        if self.cols:  # if column names have been seen
            if type(t) != Row:
                t = Row(t)  # ensure t is a row
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Col(t)

    def clone(self, init={}):
        def helper(x):
            data.add(x)
        data = Data([self.cols.names])
        self.l.map(init, helper)
        return data

    def stats(self, what, cols, nPlaces):
        def fun(k, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()

            return col.rnd(val, nPlaces), col.txt

        return self.l.kap(cols or self.cols.y, fun)

    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        for col in cols or self.cols.x:
            n += 1
            d += pow(col.dist(row1.cells[col.at],
                     row2.cells[col.at]), config.the['p'])
        return pow(d / n, 1 / config.the['p'])

    def around(self, row1, rows=None, cols=None):

        def helper(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        # return l.sort(l.map(rows or self.rows, helper), l.lt("dist"))
        r = self.l.map(rows or self.rows, helper)
        return self.l.sort(self.l.map(rows or self.rows, helper), lambda x: x['dist'])

    def half(self, rows=None, cols=None, above=None):

        # imports from other functions

        def project(row):
            return {'row': row, 'dist': self.nu.cosine(dist(row, A), dist(row, B), c)}

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        rows = rows or self.rows
        some = self.l.many(rows, config.the['Sample'])
        A = above or self.l.any(some)
        b = self.around(A, some)
        B = self.around(A, some)[
            int((config.the['Far'] * len(rows)) // 1)]['row']
        c = dist(A, B)

        left, right = [], []

        for n, tmp in enumerate(self.l.sort(self.l.map(rows, project), lambda x: x['dist'])):
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])

        return left, right, A, B, mid, c

    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows)**config.the["min"]
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        
        if len(rows) > 2*min:
            left, right, node["A"], node["B"], node["mid"], c = self.half(rows,cols,above)
            
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
            
            node["left"]  = self.sway(left,  min, cols, node["A"])
        
        return node

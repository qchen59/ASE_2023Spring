from utils import csv
from row import Row
from col import Col
from lists import Lists
import math


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

    def clone(self, init={}):
        data = Data([self.cols.names])
        self.l.map(init, lambda x: data.add(x))
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

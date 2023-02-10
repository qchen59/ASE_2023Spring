import config
import math
import utils
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
            utils.csv(src, helper)
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

    # clone the data
    def clone(self, init={}):
        def helper(x):
            data.add(x)
        data = Data([self.cols.names])
        self.l.map(init, helper)
        return data
    # calculate the stats (mean, stand deviations)
    def stats(self, what, cols, nPlaces):
        def fun(k, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()

            return col.rnd(val, nPlaces), col.txt

        return self.l.kap(cols or self.cols.y, fun)

    # calculate which row is better using continuous domination
    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    # calculate the distance between two rows
    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        for col in cols or self.cols.x:
            n += 1
            d += col.dist(row1.cells[col.at], row2.cells[col.at]) ** config.the['p']
        return (d / n) ** (1 / config.the['p'])

    # find the rows around (sort other rows by distance to row)
    def around(self, row1, rows=None, cols=None):
        def helper(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}
        return self.l.sort(self.l.map(rows or self.rows, helper), lambda x: x['dist'])

    # divides data using 2 far points
    def half(self, rows=None, cols=None, above=None):
        def project(row):
            x2, y = self.nu.cosine(dist(row, A), dist(row, B), c)
            row.x = row.x or x2
            row.y = row.y or y
            return {'row': row, 'x': x2, 'y': y}

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        rows = rows or self.rows
        A = above or self.l.any(rows)
        B = self.furthest(A, rows)['row']
        c = dist(A, B)
        left, right = [], []
        sm = self.l.sort(self.l.map(rows, project), lambda x: x['x'])
        for n, tmp in enumerate(sm,1):
            if n <= len(rows)// 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        return left, right, A, B, mid, c

    # returns best half, recursively
    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows)**config.the["min"]
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2*min:
            left, right, node["A"], node["B"], node["mid"], c = self.half(rows,cols,above)
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]

            node["left"] = self.sway(left,  min, cols, node["A"])

        return node

    # returns rows, recursively halved
    def cluster(self, rows=None, cols=None, above=None):
        rows = rows or self.rows
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows) >= 2:
            left, right, node["A"], node["B"], node["mid"], node['c'] = self.half(rows, cols, above)
            node["left"] = self.cluster(left, cols, node["A"])
            node["right"] = self.cluster(right, cols, node["B"])
        return node

    # sort other `rows` by distance to `row`
    def furthest(self, row1, row2, cols=None):
        t = self.around(row1, row2, cols)
        # print("t", t)
        return t[len(t) - 1]

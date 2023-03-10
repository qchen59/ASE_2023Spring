import config
import math
from utils import csv
from row import Row
from col import Col
import lists
import config
import math
import numerics
import functools


class Data:
    def __init__(self, src, rows=None) -> None:
        self.rows = []
        self.cols = None

        def helper(x):
            self.add(x)
            # return None, None

        if type(src) == str:
            csv(src, helper)
        else:
            lists.map(src, helper)

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
        lists.map(init, helper)
        return data

    # calculate the stats (mean, stand deviations)

    def stats(self, what='mid', cols=None, nPlaces=2):
        def fun(k, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()
            return col.rnd(val, nPlaces), col.txt

        return lists.kap(cols or self.cols.y, fun)

    # calculate which row is better using continuous domination
    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)

    def better2(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) - s2 / len(ys)

    def betters(self, n):
        def helper(item1, item2):
            return self.better2(item1, item2)
        # tmp = lists.sort(self.rows, helper)
        tmp = self.rows
        cmp = functools.cmp_to_key(helper)
        tmp.sort(key=cmp)

        # return  n and slice(tmp,1,n), slice(tmp,n+1)  or tmp  end
        if n:
            return tmp[:n], tmp[n:]
        else:
            return tmp


    # calculate the distance between two rows
    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        for col in cols or self.cols.x:
            n += 1
            d += col.dist(row1.cells[col.at],
                          row2.cells[col.at]) ** config.the['p']
        return (d / n) ** (1 / config.the['p'])

    # find the rows around (sort other rows by distance to row)
    def around(self, row1, rows=None, cols=None):
        def helper(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        return lists.sort(lists.map(rows or self.rows, helper), lambda x: x['dist'])

    # divides data using 2 far points
    def half(self, rows=None, cols=None, above=None):
        def project(row):
            x2, y = numerics.cosine(dist(row, A), dist(row, B), c)
            return {'row': row, 'dist': x2}

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        rows = rows or self.rows
        some = lists.many(rows, config.the['Halves'])
        A = (config.the['Reuse'] and above) or lists.any(some)
        B = self.around(A, some)[
            int((config.the['Far'] * len(some)) // 1)-1]['row']
        c = dist(A, B)
        # print(int((config.the['Far'] * len(some)) // 1), A,B,c)
        left, right = [], []
        for n, tmp in enumerate(lists.sort(lists.map(rows, project), lambda x: x['dist']), 1):
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        return left, right, A, B, mid, c

    # divides data using 2 far points
    def half2(self, rows=None, cols=None, above=None):
        def project(row):
            x2, y = numerics.cosine(dist(row, A), dist(row, B), c)
            return {'row': row, 'dist': x2}

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        rows = rows or self.rows
        some = lists.many(rows, config.the['Halves'])
        A = (config.the['Reuse'] and above) or lists.any(some)
        B = self.around(A, some)[
            int((config.the['Far'] * len(some)) // 1)-1]['row']
        c = dist(A, B)
        # print(int((config.the['Far'] * len(some)) // 1), A,B,c)
        left, right = [], []
        # print(lists.sort(lists.map(rows, project), lambda x: x['dist']))
        for n, tmp in enumerate(lists.sort(lists.map(rows, project), lambda x: x['dist']), 1):
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])

        if config.the['Reuse'] and above:
            evals = 1
        else:
            evals = 2
        # print("-----------------")
        return left, right, A, B, mid, c, evals


    # returns best half, recursively
    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows) ** config.the["min"]
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["mid"], c = self.half(
                rows, cols, above)
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]

            node["left"] = self.sway(left, min, cols, node["A"])

        return node

    def sway2(self):
        def worker(rows, worse, above=None):
            if len(rows) <= len(self.rows) ** config.the['min']:
                return rows, lists.many(worse, config.the['rest'] * len(rows))
            else:
                l, r, A, B, m, c = self.half(rows, self.cols.x, above)
                if self.better(B, A):
                    l, r, A, B, = r, l, B, A
                lists.map(r, lambda x: worse.append(x))
                return worker(l, worse, A)

        best, rest = worker(self.rows, [])
        return self.clone(best), self.clone(rest)

    def sway3(self):
        def worker(rows, worse, evals0, above=None):
            if len(rows) < len(self.rows) ** config.the['min']:
                return rows, lists.many(worse, config.the['rest'] * len(rows)), evals0
            else:
                l, r, A, B, m, c, evals = self.half2(rows, self.cols.x, above) # half() needs HW6 adjustment to return evals
                # print(A,B,c,evals)
                if self.better(B, A):
                    l, r, A, B = r, l, B, A
                # print(l)
                # print("-------")
                lists.map(r, lambda x: worse.append(x))
                return worker(l, worse, evals + evals0, A)

        best, rest, evals = worker(self.rows, [], 0)
        # print(best)
        # print("-------")
        # print(rest)
        # print("-------")
        # print(evals)
        # print("-------")
        return self.clone(best), self.clone(rest), evals

    # returns rows, recursively halved
    def cluster(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows) ** config.the['min']
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["mid"], c = self.half(
                rows, cols, above)
            node["left"] = self.cluster(left, min, cols, node["A"])
            node["right"] = self.cluster(right, min, cols, node["B"])
        return node

def read(sfile):
    data = Data()

    def helper(x):
        data.add(x)

    csv(sfile, helper)
    return data
import copy
from numerics import Numerics


class Lists:
    def __init__(self) -> None:
        self.nu = Numerics()

    def returnHandler(self, value, n=1):
        # for None
        if value is None:
            return [None]*n

        # for list, set, dict, tuple
        if type(value) in [list, set, dict, tuple]:
            values_to_return = []
            remaining = n
            if n <= len(value):
                values_to_return = [value]
                remaining -= 1

            if remaining != 0:
                while remaining != 0:
                    values_to_return.append(None)
                    remaining -= 1

            return values_to_return

        values_to_return = [value]
        remaining = n-1
        # for others (int,str,etc)
        if remaining != 0:
            while remaining != 0:
                values_to_return.append(None)
                remaining -= 1

    # map a function `fun`(v) over list (skip nil results)
    def map(self, table, fun):
        newTable = []
        for k, v in enumerate(table):
            v, k = self.returnHandler(fun(v), 2)
            if k is None:
                newTable.append(v)
            else:
                newTable[k] = v
        return newTable

    def kap(self, table, fun):
        newTable = {}
        for k, v in enumerate(table):
            v, k = fun(k, v)
            if k is None:
                newTable[len(newTable) + 1] = v
            else:
                newTable[k] = v
        return newTable

    # return t, sorted by fun (default= <)
    def sort(self, table, fun=None):
        return sorted(table, key=fun)

    # return list of table keys, sorted
    # -- anonymous function acquires keys from table t
    # -- kap() is called to get a new table
    # -- sort() is called to sort new table in ascending default order
    def keys(self, table):
        return self.sort(self.kap(table, lambda k, _: k))

    # return a function that sorts ascending on `x`
    def lt(x):
        def helper(a, b):
            return a[x] < b[x]

        return helper

    # pick a random item from the table
    def any(self, table):
        a = self.nu.rint(len(table)) - 1
        return table[a]

    # randomly pick n items from the table and store in a new table
    def many(self, table, n):
        newTable = []
        for i in range(n):
            newTable.append(self.any(table))
        return newTable

    # make a deep copy
    def copy(self, t):
        return copy.deepcopy(t)

    def last(self, t):
        return t[len(t)-1]





    #     function repgrid(sFile,     t,rows,cols)
    #   t = dofile(sFile)
    #   rows = repRows(t, transpose(t.cols))
    #   cols = repCols(t.cols)
    #   show(rows:cluster())
    #   show(cols:cluster())
    #   repPlace(rows)
    # end
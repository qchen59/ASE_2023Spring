from utils import returnHandler

from numerics import Numerics


class Lists:
    def __init__(self) -> None:
        self.nu = Numerics()

    # map a function `fun`(v) over list (skip nil results)
    def map(self, table, fun):
        newTable = []
        for k, v in enumerate(table):
            v, k = returnHandler(fun(v), 2)
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
        return table[self.nu.rint(0, len(table) - 1)]

    # randomly pick n items from the table and store in a new table
    def many(self, table, n):
        newTable = []
        for i in range(n):
            newTable.append(self.any(table))
        return newTable

from numerics import Numerics

class Lists:

    # map a function `fun`(v) over list (skip nil results)
    def map(self, table, fun):
        newTable = {}
        for k, v in table.items():
            v, k = fun(v)
            if k is None:
                newTable[len(newTable) + 1] = v
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
        table.sort(key=fun)
        return table

    # return list of table keys, sorted
    # -- anonymous function acquires keys from table t
    # -- kap() is called to get a new table
    # -- sort() is called to sort new table in ascending default order
    def keys(self, table):
        return self.sort(self.kap(table, lambda k, _: k))

    # pick a random item from the table
    def any(self, table):
        numerics = Numerics()
        return table[numerics.rint(0, len(table) - 1)]

    # randomly pick n items from the table and store in a new table
    def many(table, n):
        newTable = []
        for i in range(n):
            newTable.append(any(table))
        return newTable

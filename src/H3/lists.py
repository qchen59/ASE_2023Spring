class Lists:

    # map a function `fun`(v) over list (skip nil results)
    def map(self, table, fun):
        newTable = {}
        for k, v in enumerate(table):
            print(k, v)
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

    # return a function that sorts ascending on `x`
    def lt(x):
        def helper(a, b):
            return a[x] < b[x]

        return helper

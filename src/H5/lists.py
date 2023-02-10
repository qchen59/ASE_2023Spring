from utils import returnHandler
import numerics


# map a function `fun`(v) over list (skip nil results)
def map(table, fun):
    newTable = []
    for k, v in enumerate(table):
        v, k = returnHandler(fun(v), 2)
        if k is None:
            newTable.append(v)
        else:
            newTable[k] = v
    return newTable


def kap(table, fun):
    newTable = {}
    for k, v in enumerate(table):
        v, k = fun(k, v)
        if k is None:
            newTable[len(newTable) + 1] = v
        else:
            newTable[k] = v
    return newTable


# return t, sorted by fun (default= <)
def sort(table, fun=None):
    return sorted(table, key=fun)


# return list of table keys, sorted
# -- anonymous function acquires keys from table t
# -- kap() is called to get a new table
# -- sort() is called to sort new table in ascending default order
def keys(table):
    return sort(kap(table, lambda k, _: k))


# return a function that sorts ascending on `x`
def lt(x):
    def helper(a, b):
        return a[x] < b[x]

    return helper


# pick a random item from the table
def any(table):
    a = numerics.rint(len(table)) - 1
    return table[a]


# randomly pick n items from the table and store in a new table
def many(table, n):
    newTable = []
    for i in range(n):
        newTable.append(any(table))
    return newTable

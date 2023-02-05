from utils import returnHandler, show
import copy
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
<<<<<<< HEAD
=======
         
>>>>>>> origin/niraj_hw4

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

def repCols(self, cols):

    for col in cols:
        col[-1] = str(col[0]) + ":" + str(col[-1])
        for j in range(1, len(col)):
            col[j-1] = col[j]
        col = col[:-1] # remove last element

    def numPlusStr(k, v):
        return "Num" + str(k)

    #insert into the cols table using helper function
    cols.insert(0, self.kap(cols[0], numPlusStr)) # Need another way to insert() into list of cols
    cols[0][len(cols[0]) - 1] = "thingX"
    return cols


def repPlace(self, data, n, g, max_x, max_y, x, y, c):
    n, g = 20, {}
    g = [ [' ' for j in range(n+1)] for i in range(n+1)]
    max_y = 0
    print('')

    for r, row in enumerate(data['rows']):
        c = chr(64 + r)
        print(c, row['cells'][-1])
        x, y = int(row['x'] * n), int(row['y'] * n)
        max_y = max(max_y, y + 1)
        g[y + 1][x + 1] = c
    print('')

    for y in range(max_y):
        print(g[y])


def repGrid(self, sFile, table):
    # table = doFile(sFile)  -- Require a parsing function in utils.py that reads the repgrid1.csv file into a dict
    rows = self.repRows(table, self.transpose(table.cols))
    cols = self.repCols(table.cols)
    show(rows.cluster())
    show(cols.cluster())

    self.repPlace(rows)




#     function repgrid(sFile,     t,rows,cols)
#   t = dofile(sFile)
#   rows = repRows(t, transpose(t.cols))
#   cols = repCols(t.cols)
#   show(rows:cluster())
#   show(cols:cluster())
#   repPlace(rows)
# end
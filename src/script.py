#script.lua -> script.py

import math

# Numerics Class
class Numerics:
    def __init__(self,seed=937162211):
        self.Seed = seed

    def rint(self,lo=0, hi=1): # n ; a integer lo..hi-1
        return math.floor(0.5 + self.rand(lo, hi))

    def rand(self,lo=0, hi=1): # n; a float "x" lo<=x < x
        self.Seed = (16807 * self.Seed) % 2147483647
        return lo + (hi - lo) * self.Seed / 2147483647

    def rnd(self,n, nPlaces=3): # num. return `n` rounded to `nPlaces`
        mult = 10 ** nPlaces
        return math.floor(n * mult + 0.5) / mult


# Lists Class
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

    # map a function `fun`(k, v) over list (skip nil results)
    def kap(self, table, fun):
        newTable = {}
        for k, v in table.items():
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
    
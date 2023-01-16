# script.lua -> script.py
import sys
import math
import re

# Global Variable List
the = {'seed': 937162211}
help = "script.py : an example script with help text and a test suite\nUSAGE:   script.py  [OPTIONS] [-g ACTION]\nOPTIONS:\n-d  --dump  on crash, dump stack = false\n-g  --go    start-up action      = data\n-h  --help  show help            = false\n-s  --seed  random number seed   = 937162211\nACTIONS:\n"


class Sym:
    def __init__(self) -> None:
        self.n = 0
        self.has = {}
        self.most, self.mode = 0, None

    def add(self, x):
        if x != "?":
            self.n += 1
            # increase count of symbol in dictionary "has"
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self, e=0):
        def fun(p):
            return p * math.log(p, 2)

        for _, n in self.has.items():
            e += fun(n / self.n)

        return -e


# Numerics Class
class Numerics:
    def __init__(self):
        self.Seed = the["seed"]

    def rint(self, lo=0, hi=1):  # n ; a integer lo..hi-1
        return math.floor(0.5 + self.rand(lo, hi))

    def rand(self, lo=0, hi=1):  # n; a float "x" lo<=x < x
        self.Seed = (16807 * self.Seed) % 2147483647
        return lo + (hi - lo) * self.Seed / 2147483647

    def rnd(self, n, nPlaces=3):  # num. return `n` rounded to `nPlaces`
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

    # -- NUM


# -- Summarizes a stream of numbers.
class Num:
    def __init__(self):
        # number of numbers
        self.n = 0
        # mean
        self.mu = 0
        self.m2 = 0
        # the smallest number
        self.lo = float('inf')
        # largest number
        self.hi = float('-inf')

    # add `n`, update lo,hi and stuff needed for standard deviation
    def add(self, n):
        if n != "?":
            # add one more number
            self.n += 1
            # difference = new adding number - mean of number stream
            d = n - self.mu
            # update the new mean
            self.mu += d / self.n
            # For stand deviation
            self.m2 += d * (n - self.mu)
            # Update the smallest
            self.lo = min(n, self.lo)
            # Update the largest
            self.hi = max(n, self.hi)

    # return mean
    def mid(self):
        return self.mu

    # return standard deviation using Welford's algorithm http://t.ly/nn_W
    def div(self):
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return pow(self.m2 / (self.n - 1), 0.5)


def coerce(s: str):
    try:
        # check if boolean true
        if s.lower() == 'true':
            return True
        # check if boolean false
        elif s.lower() == 'false':
            return False
        try:
            # cast to int
            return int(s)
        except Exception as e:
            try:
                # cast to float
                return float(s)
            except Exception as e:
                # remove whitespaces
                return s.strip()
    except Exception as e:
        # any other exception, return as is
        return s


# -- `main` fills in the settings, updates them from the command line, runs
# -- the start up actions (and before each run, it resets the random number seed and settongs);
# -- and, finally, returns the number of test crashed to the operating system.

class Main:
    # parse help string to extract a table of options
    def settings(self, s):
        t = {}
        result = re.findall("[\n]\s*[-]\S+\s*[-][-](\S+)[^=]*[=]\s*(\S+)", s)
        for k, v in result:
            t[k] = v
        return t

    # update key,val in `t` from command-line flags
    def cli(self, options):
        for k, v in options.items():
            for n, x in enumerate(sys.argv):
                # If the command line argument equals to the option
                if x == "-" + k[0] or x == "--" + k:
                    if v == "false":
                        v = "true"
                    elif v == "true":
                        v = "false"
                    else:
                        v = sys.argv[n + 1]
            options[k] = coerce(v)
        return options

    # -- `main` fills in the settings, updates them from the command line, runs
    # -- the start up actions (and before each run, it resets the random number seed and settongs);
    # -- and, finally, returns the number of test crashed to the operating system.
    def main(self, help, funs):
        global the
        saved = {}
        fails = 0
        for k, v in self.cli(self.settings(help)).items():
            the[k] = v
            saved[k] = v
        if the["help"]:
            print(help)
        else:
            for what, fun in funs.items():
                if the["go"] == "all" or what == the["go"]:
                    for k, v in saved.items():
                        the[k] = v
                    # Check the global variable Seed for Numeric
                    # the["seed"] = int(the["seed"])
                    if not funs[what]():
                        fails += 1
                        print("❌ fail:", what)
                    else:
                        print("✅ pass:", what)


# Example Test Cases
egs = {}


# register an example
def eg(key, str, fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, str)


def numTest():
    num = Num()
    numeric = Numerics()
    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)
    return 11 / 7 == num.mid() and 0.787 == numeric.rnd(num.div())


def randTest():
    # Generate 2 nums from Num()
    num1, num2 = Num(), Num()

    numeric = Numerics()
    # Get set the seed from global setting
    numeric.Seed = the['seed'];

    # Add random numbers
    for i in range(10 ** 3):
        num1.add(numeric.rand(0, 1))

    # get the seed from global setting again (rand() alters the seed in class)
    numeric.Seed = the['seed'];

    # Add random numbers
    for i in range(10 ** 3):
        num2.add(numeric.rand(0, 1))

    # Test comparison
    m1, m2 = numeric.rnd(num1.mid(), 10), numeric.rnd(num2.mid(), 10)
    return m1 == m2 and .5 == numeric.rnd(m1, 1)


def symTest():
    sym = Sym()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    numeric = Numerics()
    return "a" == sym.mid() and 1.379 == numeric.rnd(sym.div())


def theTest():
    print(the)
    return the


eg("the", "show settings", theTest)
eg("sym", "check syms", symTest)
eg("rand", "generate, reset, regenerate same", randTest)
eg("num", "check nums", numTest)
m = Main()
m.main(help, egs)

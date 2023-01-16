#script.lua -> script.py

import math
import re

# Global Variable List
the = {'seed': 937162211}
help = "script.py : an example script with help text and a test suite\nUSAGE:   script.py  [OPTIONS] [-g ACTION]\nOPTIONS:\n-d  --dump  on crash, dump stack = false\n-g  --go    start-up action      = data\n-h  --help  show help            = false\n-s  --seed  random number seed   = 937162211\nACTIONS:\n"

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
            options[k] = v
        return options

    # -- `main` fills in the settings, updates them from the command line, runs
    # -- the start up actions (and before each run, it resets the random number seed and settongs);
    # -- and, finally, returns the number of test crashed to the operating system.
    def main(self, options, help, funs):
        saved = {}
        fails = 0
        for k, v in self.cli(self.settings(help)).items():
            options[k] = v
            saved[k] = v
        if options["help"] == "true":
            print(help)
        else:
            for what, fun in funs.items():
                if options["go"] == "all" or what == options["go"]:
                    for k, v in saved.items():
                        options[k] = v
                    # Check the global variable Seed for Numeric
                    the["seed"] = int(options["seed"])
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
    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)
    # TODO: add 0.787 == rnd(num.div())
    return 11 / 7 == num.mid()

    # Testing the Random functions within Numerics class
    def randTest():
        # Generate 2 nums from Num() [defined by Qiuyu]
        num1,num2 = Num(),Num()

        # Get set the seed from global setting
        Numerics.Seed = the['seed'];

        # Add random numbers
        for i in range(10**3):
            num1.add(Numerics.rand(0,1))

        # get the seed from global setting again (rand() alters the seed in class)
        Numerics.Seed = the['seed'];

        # Add random numbers
        for i in range(10**3):
            num2.add(Numerics.rand(0,1))

        # Test comparison
        m1,m2 = Numerics.rnd(num1.mid(),10), Numerics.rnd(num2.mid(),10)
        return m1 == m2 and .5 == Numerics.rnd(m1,1)

    # eg function defined by Qiuyu
    # eg("rand", "generate, reset, regenerate same", randTest())

eg("num", "check nums", numTest)
m = Main()
m.main(the, help, egs)
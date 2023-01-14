# script.lua -> script.py
import sys
import re

the = {}
help = "script.py : an example script with help text and a test suite\nUSAGE:   script.lua  [OPTIONS] [-g ACTION]\nOPTIONS:\n-d  --dump  on crash, dump stack = false\n-g  --go    start-up action      = data\n-h  --help  show help            = false\n-s  --seed  random number seed   = 937162211\nACTIONS:"
b4 = {}
# -----------------------------------------------------------------------------------------

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
        return (self.m2 < 0 or self.n < 2) and 0 or pow(self.m2 / (self.n - 1), 0.5)


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
        for k, v in options:
            for n, x in sys.argv:
                if x[0] == "-" or x == "--":
                    v = v == "false" and "true" or v == "true" and "false" or sys.argv[n + 1]
            options[k] = v
        return options

# -- `main` fills in the settings, updates them from the command line, runs
# -- the start up actions (and before each run, it resets the random number seed and settongs);
# -- and, finally, returns the number of test crashed to the operating system.
    def main(self, options, funs):
        saved = {}
        fails = 0
        for k, v in self.cli(self.settings(help)):
            options[k] = v
            saved[k] = v
        if options["help"]:
            print(help)
        else:
            for what, fun in funs:
                if options["go"] == "all" or what == options["go"]:
                    for k, v in saved:
                        options[k] = v
                    Seed = options.seed
                    if not funs[what]():
                        fails += 1
                        print("❌ fail:", what)
                    else:
                        print("✅ pass:", what)
# script.lua -> script.py
import sys
import re

the = {}
help = "script.py : an example script with help text and a test suite\nUSAGE:   script.py  [OPTIONS] [-g ACTION]\nOPTIONS:\n-d  --dump  on crash, dump stack = false\n-g  --go    start-up action      = data\n-h  --help  show help            = false\n-s  --seed  random number seed   = 937162211\nACTIONS:"


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
                    Seed = options["seed"]
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


eg("num", "check nums", numTest)
m = Main()
m.main(the, help, egs)

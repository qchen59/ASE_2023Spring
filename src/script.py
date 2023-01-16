#script.lua -> script.py
import math
import re
import sys

the = {}
help = "script.py : an example script with help text and a test suite\nUSAGE:   script.py  [OPTIONS] [-g ACTION]\nOPTIONS:\n-d  --dump  on crash, dump stack = false\n-g  --go    start-up action      = data\n-h  --help  show help            = false\n-s  --seed  random number seed   = 937162211\nACTIONS:\n"


class Sym:
    def __init__(self) -> None:
        self.n = 0
        self.has = {}
        self.most, self.mode = 0,None

    def add(self, x):
        if x != "?": 
            self.n += 1 
            # increase count of symbol in dictionary "has"
            self.has[x] = 1 + self.has.get(x,0)
            if self.has[x] > self.most:
                self.most,self.mode = self.has[x], x

    def mid(self):
        return self.mode
    
    def div(self, fun, e):
        def fun(p):
            return p*math.log(p,2)
        
        e = 0
        for _,n in self.has.items():
            e += fun(n/self.n)
        
        return -e
    

# Strings
def coerce(s:str):
    try:
        # check if boolean true
        if s.lower()=='true':
            return True
        # check if boolean false
        elif s.lower()=='false':
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


def symTest():
    sym = Sym()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x)
    return "a"==sym.mid() #and 1.379 == rnd(sym:div())end)


eg("sym", "check syms", symTest)
m = Main()
m.main(the, help, egs)

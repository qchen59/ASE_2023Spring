# script.lua -> script.py
from utils import eg, cli, settings
from tests import theTest, symTest, randTest, numTest, csvTest, dataTest, statsTest, cloneTest, aroundTest, halfTest, clusterTest
import config


class Main:
    # parse help string to extract a table of options

    # -- `main` fills in the settings, updates them from the command line, runs
    # -- the start up actions (and before each run, it resets the random number seed and settongs);
    # -- and, finally, returns the number of test crashed to the operating system.
    def main(self, help, funs):
        # global the
        saved = {}
        fails = 0
        for k, v in cli(settings(help)).items():
            config.the[k] = v
            saved[k] = v
        if config.the["help"]:
            print(help)
        else:
            for what, fun in funs.items():
                if config.the["go"] == "all" or what == config.the["go"]:
                    for k, v in saved.items():
                        config.the[k] = v
                    # Check the global variable Seed for Numeric
                    # the["seed"] = int(the["seed"])
                    if not funs[what]():
                        fails += 1
                        print("❌ fail:", what)
                    else:
                        print("✅ pass:", what)


if __name__ == '__main__':

    eg("the", "show settings", theTest)
    eg("sym", "check syms", symTest)
    # eg("rand", "generate, reset, regenerate same", randTest)
    eg("num", "check nums", numTest)
    eg("csv", "read from csv", csvTest)
    eg("data", "read DATA csv", dataTest)
    eg("stats", "stats from DATA", statsTest)
    eg("clone", "duplicate structure", cloneTest)
    eg("around", "sorting nearest neighbors", aroundTest)
    eg("half", "1-level bi-clustering", halfTest)
    eg("cluster", "N-level bi-clustering", clusterTest)
    m = Main()
    m.main(config.help, config.egs)

# script.lua -> script.py
from utils import eg, cli, settings
from tests import theTest, symTest, randTest, numTest, csvTest, dataTest, statsTest, cloneTest, aroundTest, halfTest, optimizeTest, clusterTest, cliffsTest, binsTest, swayTest
import config
import numerics


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
                    numerics.Seed = config.the['seed']
                    # Check the global variable Seed for Numeric
                    # the["seed"] = int(the["seed"])
                    if not funs[what]():
                        fails += 1
                        print("❌ fail:", what)
                    else:
                        print("✅ pass:", what)


if __name__ == '__main__':
    eg("clone", "duplicate structure", cloneTest)
    eg("around", "sorting nearest neighbors", aroundTest)
    eg("cluster", "N-level bi-clustering", clusterTest)
    eg("data", "read DATA csv", dataTest)
    eg("half", "1-level bi-clustering", halfTest)
    eg("num", "check nums", numTest)
    eg("optimize", "semi-supervised optimization", optimizeTest)
    eg("the", "show settings", theTest)
    eg("sym", "check syms", symTest)
    eg("cliffs", "stats tests", cliffsTest)
    eg("rand", "generate, reset, regenerate same", randTest)
    eg("csv", "read from csv", csvTest)
    eg("stats", "stats from DATA", statsTest)
    eg("bins", "find deltas between best and rest", binsTest)
    eg("sway", "optimizing", swayTest)
    m = Main()
    m.main(config.help, config.egs)

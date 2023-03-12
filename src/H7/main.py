# script.lua -> script.py
from utils import eg, cli, settings
import config
from tests import sampleTest, numTest, guassTest

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
                    if not funs[what]():
                        fails += 1
                        print("❌ fail:", what)
                    else:
                        print("✅ pass:", what)


if __name__ == '__main__':
    eg("sample", "Test the sampling", sampleTest)
    eg("num", "Test the num", numTest)
    eg("guass", "Test the guassian", guassTest)
    m = Main()
    m.main(config.help, config.egs)
    # print(config.the)

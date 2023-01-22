import config
from num import Num
from sym import Sym
from numerics import Numerics
from utils import csv


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
    numeric.Seed = config.the['seed']

    # Add random numbers
    for i in range(10 ** 3):
        num1.add(numeric.rand(0, 1))

    # get the seed from global setting again (rand() alters the seed in class)
    numeric.Seed = config.the['seed']

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
    print(config.the)
    return config.the


def csvTest():
    n = 0

    def csvHelper(t):
        nonlocal n
        n += len(t)

    csv(config.the['file'], csvHelper)
    return n == 8 * 399

import config
from num import Num
from sym import Sym
from numerics import Numerics
from data import Data
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


def dataTest():
    data = Data(config.the['file'])
    return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[1].at == 1 and len(data.cols.x) == 4


def statsTest():
    data = Data(config.the['file'])
    print("x", "mid", data.stats("mid", data.cols.x, 2))
    print("div", data.stats("div", data.cols.x, 2))
    print("y", "mid", data.stats("mid", data.cols.y, 2))
    print("div", data.stats("div", data.cols.y, 2))
    return True


def cloneTest():
    data1 = Data(config.the['file'])
    data2 = data1.clone(data1.rows)
    return len(data1.rows) == len(data2.rows) and data1.cols.y[1].w == data2.cols.y[1].w and data1.cols.x[1].at == data2.cols.x[1].at and len(data1.cols.x) == len(data2.cols.x)


def aroundTest():
    data = Data(config.the['file'])
    print(0, 0, data.rows[1].cells)
    nu = Numerics()
    for n, t in enumerate(data.around(data.rows[1])):
        if n % 50 == 0:
            print(n, nu.rnd(t.dist, 2), t.row.cells)
    return True

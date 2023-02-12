import config
from num import Num
from sym import Sym
import numerics
from data import Data
from utils import csv, show
import lists
from utils import returnHandler
from discretization import bins, value


def numTest():
    num = Num()
    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)
    return 11 / 7 == num.mid() and 0.787 == numerics.rnd(num.div())


def randTest():
    # Generate 2 nums from Num()
    num1, num2 = Num(), Num()
    numerics.Seed = config.the['seed']
    # Add random numbers
    for i in range(10 ** 3):
        num1.add(numerics.rand(0, 1))

    # get the seed from global setting again (rand() alters the seed in class)
    numerics.Seed = config.the['seed']

    # Add random numbers
    for i in range(10 ** 3):
        num2.add(numerics.rand(0, 1))

    # Test comparison
    m1, m2 = numerics.rnd(num1.mid(), 10), numerics.rnd(num2.mid(), 10)
    return m1 == m2 and .5 == numerics.rnd(m1, 1)


def symTest():
    sym = Sym()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    return "a" == sym.mid() and 1.379 == numerics.rnd(sym.div())


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
    return len(data1.rows) == len(data2.rows) and data1.cols.y[0].w == data2.cols.y[0].w and data1.cols.x[0].at == \
        data2.cols.x[0].at and len(data1.cols.x) == len(data2.cols.x)


def aroundTest():
    data = Data(config.the['file'])
    print(0, 0, data.rows[0].cells)
    p = data.around(data.rows[0])
    for n, t in enumerate(data.around(data.rows[0])):
        if (n + 1) % 50 == 0:
            print(n + 1, numerics.rnd(t['dist'], 2), t['row'].cells)
    return True


def halfTest():
    data = Data(config.the['file'])
    left, right, A, B, mid, C = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells, C)
    print(mid.cells)
    print(B.cells)
    return True


def optimizeTest():
    data = Data(config.the['file'])
    show(data.sway(), "mid", data.cols.y, 1)
    return True


def clusterTest():
    data = Data(config.the['file'])
    show(data.cluster(), "mid", data.cols.y, 1)
    return True


def cliffsTest():
    assert numerics.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [
                                8, 7, 6, 2, 5, 8, 7, 3]) == False
    assert numerics.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [
                                9, 9, 7, 8, 10, 9, 6]) == True
    t1, t2 = [], []
    for i in range(1000):
        t1.append(numerics.rand())
    for i in range(1000):
        t2.append(numerics.rand()**0.5)
    assert numerics.cliffsDelta(t1, t1) == False
    assert numerics.cliffsDelta(t1, t2) == True
    diff, j = False, 1.0
    while not diff:
        t3 = lists.map(t1, lambda x: x*j)
        diff = numerics.cliffsDelta(t1, t3)
        print(">", numerics.rnd(j), diff)
        j *= 1.025
    return True


def binsTest():
    data: Data = Data.read(config.the.file)
    best, rest = returnHandler(data.sway())
    n: numerics = numerics()
    print('all', '', '', '', {'best': len(best), 'rest': len(rest)})
    b4 = None
    for k, t in enumerate(bins(data.cols.x, {'best': best.rows, 'rest': rest.rows})):
        for _, range in enumerate(t):
            if range.txt != b4:
                print()
            b4 = range.txt
            print(range.txt, range.lo, range.hi, n.rnd(
                value(range.y.has, len(best.rows), len(rest.rows), "best")), range.y.has)

import config
from num import Num
from sym import Sym
from numerics import Numerics
from data import Data
from utils import csv, show,repCols, repRows, transpose, repPlace, repgrid
from lists import Lists

l = Lists()


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
    return len(data1.rows) == len(data2.rows) and data1.cols.y[0].w == data2.cols.y[0].w and data1.cols.x[0].at == \
           data2.cols.x[0].at and len(data1.cols.x) == len(data2.cols.x)


def aroundTest():
    data = Data(config.the['file'])
    print(0, 0, data.rows[0].cells)
    nu = Numerics()
    p = data.around(data.rows[0])
    for n, t in enumerate(data.around(data.rows[0])):
        if (n + 1) % 50 == 0:
            print(n + 1, nu.rnd(t['dist'], 2), t['row'].cells)
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


def copyTest():
    t1 = {'a': 1, 'b': {'c': 2, 'd': [3]}}
    t2 = l.copy(t1)
    t2['b']['d'][0] = 10000
    print("b4", t1)
    print("after", t2)
    return True

def recolsTest():
    t = repCols(exec(open(config.the['file']).read()).cols)
    # cols and rows objects
    l.map(t['cols'].all, lambda x: print(x))
    l.map(t['rows'], lambda x: print(x))
    return True

def synonymsTests():
    show(repCols(exec(open(config.the['file']).read()).cols).cluster())
    return True

def reprowsTest():
    t = exec(open(config.the['file']).read())
    rows = repRows(t, transpose(t['cols']))
    l.map(rows['cols'].all, lambda x: print(x))
    l.map(rows['rows'], lambda x: print(x))
    return True

def prototypesTest():
    t = exec(open(config.the['file']).read())
    rows = repRows(t, transpose(t['cols']))
    repPlace(rows)
    return True

def positionTest():
    t = exec(open(config.the['file']).read())
    rows = repRows(t, transpose(t['cols']))
    rows.cluster()
    repPlace(rows)
    return True

def everyTest():
    repgrid(config.the['file'])
    return True


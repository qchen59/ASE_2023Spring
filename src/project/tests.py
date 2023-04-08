from collections import defaultdict
import config
from num import Num
from sym import Sym
import numerics
from data import Data, read
from utils import csv, show
import lists
from utils import returnHandler
from discretization import bins, value, diffs
from merge import selects, showRule
from xpln import xpln
import pandas as pd


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
    col = data.cols.x[0]
    print(col.lo, col.hi, col.mid(), col.div())
    print(data.stats())
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
        t2.append(numerics.rand() ** 0.5)
    assert numerics.cliffsDelta(t1, t1) == False
    assert numerics.cliffsDelta(t1, t2) == True
    diff, j = False, 1.0
    while not diff:
        t3 = lists.map(t1, lambda x: x * j)
        diff = numerics.cliffsDelta(t1, t3)
        print(">", numerics.rnd(j), diff)
        j *= 1.025
    return True


def binsTest():
    data = Data(config.the['file'])
    # print(data)
    best, rest = data.sway2()
    print('all', '', '', '', {'best': len(best.rows), 'rest': len(rest.rows)})
    b4 = None
    b = bins(data.cols.x, {'best': best.rows, 'rest': rest.rows})
    print(f'{b=}')
    for k, t in enumerate(b):
        for _, range in enumerate(t):
            if range['txt'] != b4:
                print()
            b4 = range['txt']
            print(range['txt'], range['lo'], range['hi'], numerics.rnd(
                value(range['y'].has, len(best.rows), len(rest.rows), "best")), range['y'].has)
    return True


def swayTest():
    data = Data(config.the['file'])
    best, rest = data.sway2()
    print("\nall ", data.stats())
    print("    ", data.stats('div'))
    print("N=", len(data.rows))
    print("\nbest", best.stats())
    print("    ", best.stats('div'))
    print("N=", len(best.rows))
    print("\nrest", rest.stats())
    print("    ", rest.stats('div'))
    print("N=", len(rest.rows))
    print("\nall ~= best?", diffs(best.cols.y, data.cols.y))
    print("best ~= rest?", diffs(best.cols.y, rest.cols.y))
    return True


def xplnTest():
    data = Data(config.the['file'])
    best, rest, evals = data.sway3()
    # print(data)
    # print("-------")
    # print(best)
    # print("-------")
    # print(rest)
    # print("-------")
    # print(evals)
    # print("-------")

    rule, most = xpln(data, best, rest)
    print("\n-----------\nexplain=", showRule(rule))
    selected = selects(rule, data.rows)
    selected = [s for s in selected if s]
    data1 = data.clone(selected)
    print("all                  ", data.stats(), data.stats('div'))
    print("sway with %5s evals" % evals, best.stats(), best.stats('div'))
    print("xpln on   %5s evals" % evals, data1.stats(), data1.stats('div'))
    top, _ = data.betters(len(best.rows))
    top = data.clone(top)
    print("sort with %5s evals" %
          len(data.rows), top.stats(), top.stats('div'))
    return True


def projectTest():
    print('called project test')
    data = Data(config.the['file'])
    best, rest, evals = data.sway3()
    best2, rest2, evals2 = data.sway_project()
    rule, most = xpln(data, best, rest)
    rule2, most2 = xpln(data, best2, rest2)
    # print("*!*!*!*!*!*",rule)
    # TODO check if rule is None
    if rule and rule2:
        selected = selects(rule, data.rows)
        selected2 = selects(rule2, data.rows)
        selected = [s for s in selected if s]
        selected2 = [s for s in selected2 if s]
        data1 = data.clone(selected)
        data2 = data.clone(selected2)

        cols = {}
        top, _ = data.betters(len(best.rows))
        top = data.clone(top)
        medians = [data.stats(), best.stats(), best2.stats(), data1.stats(), data2.stats(), top.stats()]
        titles = ['all', 'sway1', 'sway2', 'xpln1', 'xpln2', 'top']

        for median in medians:
            for key in median:
                if key not in cols:
                    # cols[key] = [title]
                    cols[key] = []
                cols[key].append(median[key])
        cols['title'] = titles

        df_cols = pd.DataFrame.from_dict(cols)
        df_cols.set_index('title', inplace=True)
        print(df_cols)
        print('--------------------------------------------')

        return df_cols
    else:
        return None

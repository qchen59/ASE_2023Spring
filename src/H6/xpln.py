from lists import map, sort, gt
from numerics import rnd
import merge
from discretization import bins, value
from data import Data

FAIL = '\033[91m'
ENDC = '\033[0m'
from merge import showRule


def RULE(ranges, maxSize):
    t = {}
    for range in ranges:
        if range['txt'] not in t:
            t[range['txt']] = []
        t[range['txt']].append({'lo': range['lo'], 'hi': range['hi'], 'at': range['at']})
    return prune(t, maxSize)


def prune(rule, maxSize):
    # print(f'{FAIL}{type(rule)=}{ENDC}')
    n = 0
    for txt, ranges in rule.items():
        n += 1
        # TODO: check if this is correct
        if len(ranges) == maxSize[txt]:
            n -= 1
            # rule[txt] = None
            rule.remove(txt)
    if n > 0:
        return rule

def on(x):
    return lambda t: t[x]

def firstN(sortedRanges, scoreFun):
    print("")
    map(sortedRanges, lambda r: print(r['range']['txt'], r['range']['lo'], r['range']['hi'], rnd(r['val']), r['range']['y'].has))
    first = sortedRanges[0]['val']

    def useful(range):
        if range['val'] > 0.05 and range['val'] > first / 10:
            return range

    sortedRanges = map(sortedRanges, useful)
    most, out = -1, None
    sortedRanges = [i for i in sortedRanges if i]
    for n in range(len(sortedRanges)):
        t = map(sortedRanges[:n+1], lambda x: x['range'])
        tmp, rule = scoreFun(t)
        # print("tmp",tmp, most, rule)
        if tmp and tmp > most:
            out, most = rule, tmp
    return out, most

def xpln(data, best, rest, maxSizes={}):
    def v(has: dict) -> float:
        """Contains Dictionary with keys `best` or `rest` or both.
        Example1: `{'best': 11, 'rest': 19}`
        Example2: `{'rest': 29}`

        Args:
            has (dict): Dictionary with string keys and numeric values.

        Returns:
            float: A float value.
        """
        return value(has, len(best.rows), len(rest.rows), 'best')

    def score(ranges):
        rule = RULE(ranges, maxSizes)
        if rule:
            # print("rule--------------")
            # print(rule)
            print(showRule(rule))
            bestr = merge.selects(rule, best.rows)
            restr = merge.selects(rule, rest.rows)
            bestr = [b for b in bestr if b]
            restr = [r for r in restr if r]
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr),"rest": len(restr)}), rule
        return None, None
    tmp, maxSizes = [], {}
    for _, ranges in enumerate(bins(data.cols.x,{"best": best.rows, "rest": rest.rows})):
        maxSizes[ranges[0]['txt']] = len(ranges)
        print()
        for _, range in enumerate(ranges):
            print(range['txt'], range['lo'], range['hi'])
            tmp.append({
                'range': range,
                'max': len(ranges),
                'val': v(range['y'].has)
            })
    rule, most = firstN(sorted(tmp, key=lambda x: x['val'],reverse=True), score)
    return rule, most
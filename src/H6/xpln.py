from lists import map
from numerics import rnd


def rule(ranges, maxSize):
    t = {}
    for range in ranges:
        t[range.txt] = t[range.txt] or []
        t[range.txt].append({'lo': range.lo, 'hi': range.hi, 'at': range.at})
    return prune(t, maxSize)


def prune(rule, maxSize):
    n = 0
    for txt, ranges in enumerate(rule):
        n += 1
        # TODO: check if this is correct
        if len(ranges) == maxSize[txt]:
            n -= 1
            rule[txt] = None
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
    most, out = -1
    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun(map(sortedRanges[:n], on('range')))
        if tmp and tmp > most:
            our, most = rule, tmp
    return out, most

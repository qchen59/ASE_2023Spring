from lists import map, sort, gt
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

def xpln(data, best, rest, maxSizes):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), 'best')

    def score(ranges):
        rule = RULE(ranges, maxSizes)
        if rule:
            print(showRule(rule))
            bestr = selects(rule, best.rows)
            restr = selects(rule, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({
                    "best": len(bestr),
                    "rest": len(restr)
                }), rule
    tmp, maxSizes = [], {}
    for _, ranges in enumerate(bins(data.cols.x), {"best": len(bestr), "rest": len(restr)}):
        maxSizes[ranges[0].txt] = len(ranges)
        print()
        for _, range in enumerate(ranges):
            print(range.txt, range.lo, range.hi)
            tmp.append({
                'range': range,
                'max': len(ranges),
                'val': v(range.y.has)
            })
    rule, most = firstN(sort(tmp, gt('val'), score))
    return rule, most
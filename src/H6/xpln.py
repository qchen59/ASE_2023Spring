from lists import sort, gt


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

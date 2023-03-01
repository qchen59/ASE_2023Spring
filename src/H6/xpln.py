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


import math
import config
import lists
import numerics
import sym
import merge


def diffs(nums1, nums2):
    def helper(k, nums):
        return numerics.cliffsDelta(nums.has, nums2[k].has), nums.txt

    return lists.kap(nums1, helper)

# -- Create a RANGE  that tracks the y dependent values seen in
# -- the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`.
# -- Note that the way this is used (in the `bins` function, below)
# -- for  symbolic columns, `lo` is always the same as `hi`.
def RANGE(at, txt, lo, hi=None):
    # if hi is None:
    #     hi = lo
    return {'at': at, 'txt': txt, 'lo': lo, 'hi': hi or lo, 'y': sym.Sym()}


# -- Map `x` into a small number of bins. `SYM`s just get mapped
# -- to themselves but `NUM`s get mapped to one of `the.bins` values.
# -- Called by function `bins`.
def bin(col, x):
    # print(x)
    if x == "?" or isinstance(col, sym.Sym):
        return x
    tmp = (col.hi - col.lo) / (config.the['bins'] - 1)
    if col.hi == col.lo:
        return 1
    else:
        return math.floor(x / tmp + 0.5) * tmp
# Update a RANGE to cover `x` and `y`


def extend(range, n, s):
    range['lo'] = min(n, range['lo'])
    range['hi'] = max(n, range['hi'])
    range['y'].add(s)

# -- Return self


def itself(x):
    return x

# -- Given a sorted list of ranges, try fusing adjacent items
# -- (stopping when no more fuse-ings can be found). When done,
# -- make the ranges run from minus to plus infinity
# -- (with no gaps in between).


def bins(cols, rowss):
    out = []
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                x = row.cells[col.at]
                if x != "?":
                    k = bin(col, x)
                    if k in ranges:
                        ranges[k] = ranges[k]
                    else:
                        ranges[k] = RANGE(col.at, col.txt, x)
                    extend(ranges[k], x, y)
        ranges = list(ranges.values())
        ranges = lists.sort(lists.map(ranges, itself), lambda x: x['lo'])
        if isinstance(col, sym.Sym):
            out.append(ranges)
        else:
            out.append(merge.mergeAny(ranges))
    return out


def value(has, nB=1, nR=1, sGoal=True):
    b, r = 0, 0
    for x, n in has.items():
        if x == sGoal:
            b += n
        else:
            r += n
    b, r = b / (nB + 1 / float('inf')), r / (nR + 1 / float('inf'))
    return b**2/(b+r)

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
def RANGE(at, txt, lo, hi):
    return {'at': at, 'txt': txt, 'lo': lo, 'hi': lo or hi, 'y': sym()}


# -- Map `x` into a small number of bins. `SYM`s just get mapped
# -- to themselves but `NUM`s get mapped to one of `the.bins` values.
# -- Called by function `bins`.
def bin(col, x):
    if x == "?" or isinstance(col, sym.Sym) :
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
        ranges = []
        for y, rows in enumerate(rowss):
            for row in rows:
                x = row[col.at]
                if x != "?":
                    k = bin(col, x)
                    ranges[k] = ranges[k] or RANGE(cols.at, col.txt, x)
                    extend(ranges[k],x,y)
        ranges = lists.sort(lists.map(ranges,itself), lambda x: x['lo'])
        if isinstance(col, sym.Sym):
            out.append(ranges)
        else:
            merge.mergeAny(ranges)
        return out


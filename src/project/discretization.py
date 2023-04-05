import math
import config
import lists
import numerics
import sym
import merge
from num import Num
from row import Row

FAIL = '\033[91m'
ENDC = '\033[0m'


def diffs(nums1, nums2):
    def helper(k, nums):
        return numerics.cliffsDelta(nums.has, nums2[k].has), nums.txt

    return lists.kap(nums1, helper)


# -- Create a RANGE  that tracks the y dependent values seen in
# -- the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`.
# -- Note that the way this is used (in the `bins` function, below)
# -- for  symbolic columns, `lo` is always the same as `hi`.
def RANGE(at, txt, lo, hi=None):
    """Create a RANGE  that tracks the y dependent values seen in
    the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`.
    Note that the way this is used (in the `bins` function, below)
    for  symbolic columns, `lo` is always the same as `hi`.

    Args:
        at (int): _description_
        txt (str): Example = `Volume`, `Clndrs`, etc.
        lo (int): _description_
        hi (int, optional): Defaults to None.

    Returns:
        dict: `{'at': 6, 'txt': 'origin', 'lo': 2, 'hi': 2, 'y': Sym}`
    """
    return {'at': at, 'txt': txt, 'lo': lo, 'hi': hi or lo, 'y': sym.Sym()}


# -- Map `x` into a small number of bins. `SYM`s just get mapped
# -- to themselves but `NUM`s get mapped to one of `the.bins` values.
# -- Called by function `bins`.
def bin(col, x):
    """Map `x` into a small number of bins. `SYM`s just get mapped
    to themselves but `NUM`s get mapped to one of `the.bins` values.
    Called by function `bins`.

    Args:
        col (sym.Sym | Num): Can either be Num or Sym.
        x (int):

    Returns:
        str | sym.Sym | int: Returns `int` when `col` is `Num`, else the `Sym` itself.
    """
    if x == "?" or isinstance(col, sym.Sym):
        return x
    tmp = (col.hi - col.lo) / (config.the['bins'] - 1)
    if col.hi == col.lo:
        return 1
    else:
        return math.floor(x / tmp + 0.5) * tmp
# Update a RANGE to cover `x` and `y`


def extend(range, n, s):
    """Update a RANGE to cover `x` and `y`

    Args:
        range (dict): Example = `{'at': 6, 'txt': 'origin', 'lo': 2, 'hi': 2, 'y': Sym}`
        n (int):
        s (str): Example = `rest`
    """
    range['lo'] = min(n, range['lo'])
    range['hi'] = max(n, range['hi'])
    range['y'].add(s)

# -- Return self


def itself(x):
    """Return self of same datatype.

    Args:
        x (Any): Can be any datatype.

    Returns:
        Any: Returns the same variable passed.
    """
    return x


def bins(cols, rowss):
    def with1Col(col):
        n, ranges = withAllRows(col)
        ranges = lists.sort(lists.map(ranges, itself), lambda x: x['lo'])
        if isinstance(col, sym.Sym):
            # print("is", ranges)
            return ranges
        else:
            t = merge.mergeAny2(ranges, n/config.the['bins'], config.the['d']*col.div())
            # print("not", t)
            return t

    def withAllRows(col):
        def xy(x, y):
            nonlocal n
            if x != "?":
                n += 1
                k = bin(col, x)
                if k in ranges:
                    ranges[k] = ranges[k]
                else:
                    ranges[k] = RANGE(col.at, col.txt, x)
                extend(ranges[k], x, y)

        n, ranges = 0, {}
        for y, rows in rowss.items():
            for row in rows:
                xy(row.cells[col.at], y)
        return n, ranges.values()
    # output = [o for o in lists.map(cols, with1Col) if o]

    return lists.map(cols, with1Col)

def value(has, nB=1, nR=1, sGoal=True):
    """A query that returns the score a distribution of symbols inside a SYM.

    Args:
        has (dict): Example: `{'best': 11, 'rest': 19}`
        nB (int, optional): _description_. Defaults to 1.
        nR (int, optional): _description_. Defaults to 1.
        sGoal (bool, optional): _description_. Defaults to True.

    Returns:
        float: Score of distribution of symbols in Sym.
    """
    b, r = 0, 0
    for x, n in has.items():
        if x == sGoal:
            b += n
        else:
            r += n
    b, r = b / (nB + 1 / float('inf')), r / (nR + 1 / float('inf'))

    return b**2/(b+r)

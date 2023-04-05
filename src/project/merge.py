# function mergeAny(ranges0,     noGaps)
#   function noGaps(t)
#     for j = 2,#t do t[j].lo = t[j-1].hi end
#     t[1].lo  = -m.huge
#     t[#t].hi =  m.huge
#     return t 
#   end ------
#   local ranges1,j,left,right,y = {},1
#   while j <= #ranges0 do
#     left, right = ranges0[j], ranges0[j+1]
#     if right then
#       y = merge2(left.y, right.y)
#       if y then
#         j = j+1 -- next round, skip over right.
#         left.hi, left.y = right.hi, y end end
#     push(ranges1,left)
#     j = j+1 
#   end
#   return #ranges0==#ranges1 and noGaps(ranges0) or mergeAny(ranges1) end
from copy import deepcopy
from lists import map, kap
import sym
FAIL = '\033[91m'
ENDC = '\033[0m'

def mergeAny(ranges0: list[dict]) -> list[dict]:
    """Given a sorted list of ranges, try fusing adjacent items
    (stopping when no more fuse-ings can be found). When done,
    make the ranges run from minus to plus infinity
    (with no gaps in between).

    Args:
        ranges0 (list[dict]): Example = `[{'at': 0, 'txt': 'Clndrs', 'lo': -inf, 'hi': 3, 'y': Sym}]`

    Returns:
        list[dict]: Example = `[{'at': 0, 'txt': 'Clndrs', 'lo': -inf, 'hi': 3, 'y': Sym}]`
    """

    def noGaps(t: list[dict]) -> list[dict]:
        """_summary_

        Args:
            t (list[dict]): Example = `[{'at': 0, 'txt': 'Clndrs', 'lo': -inf, 'hi': 3, 'y': Sym}]`

        Returns:
            list[dict]: Example = `[{'at': 0, 'txt': 'Clndrs', 'lo': -inf, 'hi': 3, 'y': Sym}]`
        """
        for j in range(1, len(t)):
            t[j]['lo'] = t[j - 1]['hi']
        t[0]['lo'] = float('-inf')
        t[-1]['hi'] = float('inf')
        return t

    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], None if j + 1 >= len(ranges0) else ranges0[j + 1]
        # print(right)
        # print(left)
        if right:
            y = merge2(left['y'], right['y'])
            # print(y)
            if y:
                j += 1
                left['hi'], left['y'] = right['hi'], y
        ranges1.append(left)
        j += 1
        # print(j)
    # print(len(ranges0), len(ranges1))
    return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny(ranges1)

def mergeAny2(ranges0, nSmall,nFar, noGaps=None):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j]['lo'] = t[j - 1]['hi']
        t[0]['lo'] = float('-inf')
        t[-1]['hi'] = float('inf')
        return t

    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], None if j + 1 >= len(ranges0) else ranges0[j + 1]
        # print(right)
        # print(left)
        if right:
            y = merged(left['y'], right['y'], nSmall, nFar)
            # print(y)
            if y:
                j += 1
                left['hi'], left['y'] = right['hi'], y
        ranges1.append(left)
        j += 1
        # print(j)
    # print(len(ranges0), len(ranges1))
    return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny2(ranges1,  nSmall,nFar)

def merged(col1, col2, nSmall=None, nFar=None, new=None):
    # print("merged", nSmall, nFar)
    new = merge(col1, col2)
    if (nSmall and col1.n < nSmall) or (col2.n < nSmall):
        return new
    if nFar and not isinstance(col1, sym.Sym) and abs(col1.mid() - col2.mid()) < nFar:
        return new
    if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
        return new

def merge2(col1, col2):
    isNew = merge(col1, col2)
    # print("isNew", isNew)
    # need the div() function here based on col being a NUM or SYM
    # print("new",isNew.div() )
    if isNew.div() <= (col1.div() * col1.n + col2.div() * col2.n) / isNew.n:
        return isNew
    return None

def merge(col1, col2):
    isNew = deepcopy(col1)
    if isinstance(col1, sym.Sym):
        for x, n in col2.has.items():
            isNew.add(x,n)
    else:
        for n in col2.has:
            isNew.add(n)
        isNew.lo = min(col1.lo, col2.lo)
        isNew.hi = max(col1.hi, col2.hi)
    return isNew

def showRule(rule):
    def pretty(range):
        return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]

    def merges(attr, ranges):
        # print(attr,ranges)
        return list(map(merge(sorted(ranges, key=lambda r: r['lo'])), pretty)), attr

    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j + 1] if j + 1 < len(t0) else None
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j += 1
        return t if len(t0) == len(t) else merge(t)

    return kap2(rule, merges)

def kap2(table, fun):
    newTable = {}
    for k, v in table.items():
        v, k = fun(k, v)
        if k is None:
            newTable[len(newTable) + 1] = v
        else:
            newTable[k] = v
    return newTable

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo, hi, at = range['lo'], range['hi'], range['at']
            x = row.cells[at]
            if x == "?":
                return True
            if lo == hi == x:
                return True
            if lo <= x and x < hi:
                return True
        return False
    
    def conjunction(row):
        for ranges in rule.values():
            if not disjunction(ranges, row):
                return False
        return True
    
    return map(rows, lambda r: r if conjunction(r) else None)




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
import sym
def mergeAny(ranges0, noGaps=None):
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

def merge2(col1, col2):
    isNew = merge(col1, col2)
    # print("isNew", isNew)
    ## need the div() function here based on col being a NUM or SYM
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




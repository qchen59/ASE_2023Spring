import re

from src.H2.num import Num
from src.H2.sym import Sym


class Col:
    # generate NUMs and SYMs from column names
    # t = title
    def __init__(self, t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None

        for n, s in enumerate(t):
            # If upper case, the attribute is number
            if re.search(r"^[A-Z]", s):
                col = Num(n, s)
            else:
                # If lower case, the attribute is symbol
                col = Sym(n, s)
            # push all column includes the skipped
            self.all.append(col)
            # Not skipped if not end with X
            if not re.search(r"X$", s):
                if re.search(r"!$", s):
                    self.klass = col
                if re.search(r"[!+-]$", s):
                    self.y.append(col)
                else:
                    self.x.append(col)

    # update the (not skipped) columns with details from `row`
    def add(self, i, row):
        for t in i['x']:
            for col in t:
                col.add(row.cells[col.at])
        for t in i['y']:
            for col in t:
                col.add(row.cells[col.at])

# Tests
# col = Col(['Clndrs', 'Volume', 'HpX', 'Lbs-', 'Acc+', 'Model', 'origin', 'Mpg+'])

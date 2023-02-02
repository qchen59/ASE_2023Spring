import re
from num import Num
from sym import Sym


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
    def add(self, row):
        for i in self.x:
            i.add(row.cells[i.at])
        for i in self.y:
            i.add(row.cells[i.at])


    def __repr__(self):
        return str(self.__dict__)


import math


class Sym:
    def __init__(self, at=0, txt="") -> None:
        # New added in HW2
        self.at = at
        self.txt = txt

        self.n = 0
        self.has = {}
        self.most, self.mode = 0, None

    def add(self, x):
        if x != "?":
            self.n += 1
            # increase count of symbol in dictionary "has"
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self, e=0):
        def fun(p):
            return p * math.log(p, 2)

        for _, n in self.has.items():
            e += fun(n / self.n)

        return -e

    def rnd(self, x, n):
        return x

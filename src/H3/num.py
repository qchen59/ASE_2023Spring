# -- Summarizes a stream of numbers.
import re
from numerics import Numerics


class Num:
    def __init__(self, at=0, txt=""):
        # New added in HW2
        self.at = at
        self.txt = txt

        # number of numbers
        self.n = 0
        # mean
        self.mu = 0
        self.m2 = 0
        # the smallest number
        self.lo = float('inf')
        # largest number
        self.hi = float('-inf')

        if re.search(r"-$", self.txt):
            self.w = -1
        else:
            self.w = 1

    # add `n`, update lo,hi and stuff needed for standard deviation
    def add(self, n):
        if n != "?":
            # add one more number
            self.n += 1
            # difference = new adding number - mean of number stream
            d = n - self.mu
            # update the new mean
            self.mu += d / self.n
            # For stand deviation
            self.m2 += d * (n - self.mu)
            # Update the smallest
            self.lo = min(n, self.lo)
            # Update the largest
            self.hi = max(n, self.hi)

    # return means
    def mid(self):
        return self.mu

    # return standard deviation using Welford's algorithm http://t.ly/nn_W
    def div(self):
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return pow(self.m2 / (self.n - 1), 0.5)

    def rnd(self, x, n):
        if x == "?":
            return x
        else:
            nu = Numerics()
            return nu.rnd(x, n)

    def norm(self, n):
        return n if n == "?" else (n - self.lo)/(self.hi - self.lo + 1E-32)

    def __repr__(self):
        return str(self.__dict__)

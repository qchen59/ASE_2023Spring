import math
from config import the


class Numerics:
    def __init__(self):
        self.Seed = the["seed"]

    def rint(self, lo=0, hi=1):  # n ; a integer lo..hi-1
        return math.floor(0.5 + self.rand(lo, hi))

    def rand(self, lo=0, hi=1):  # n; a float "x" lo<=x < x
        self.Seed = (16807 * self.Seed) % 2147483647
        return lo + (hi - lo) * self.Seed / 2147483647

    def rnd(self, n, nPlaces=3):  # num. return `n` rounded to `nPlaces`
        mult = 10 ** nPlaces
        return math.floor(n * mult + 0.5) / mult

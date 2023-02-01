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

    def cosine(self, a, b, c):
        x1 = (a**2 + c**2 - b**2) / (2*c) # find the x from line connecting a to b
        x2 = max(0, min(1, x1)) # x2 is x1 confined between 0 and 1
        y = (a**2 - x2**2)**0.5 # find the y from line connecting a to b
        return x2, y
 
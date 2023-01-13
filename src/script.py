#script.lua -> script.py

import math

# Numerics Class
class Numerics:
    def __init__(self,seed=937162211):
        self.Seed = seed

    def rint(self,lo=0, hi=1): # n ; a integer lo..hi-1
        return math.floor(0.5 + self.rand(lo, hi))

    def rand(self,lo=0, hi=1): # n; a float "x" lo<=x < x
        self.Seed = (16807 * self.Seed) % 2147483647
        return lo + (hi - lo) * self.Seed / 2147483647

    def rnd(self,n, nPlaces=3): # num. return `n` rounded to `nPlaces`
        mult = 10 ** nPlaces
        return math.floor(n * mult + 0.5) / mult


# local Seed,rand,rint,rnd
# Seed=937162211
# function rint(lo,hi) return math.floor(0.5 + rand(lo,hi)) end --> 

# function rand(lo,hi) --> n; a float "x" lo<=x < x
#   lo, hi = lo or 0, hi or 1
#   Seed = (16807 * Seed) % 2147483647
#   return lo + (hi-lo) * Seed / 2147483647 end

# function rnd(n, nPlaces) --> num. return `n` rounded to `nPlaces`
#   local mult = 10^(nPlaces or 3)
#   return math.floor(n * mult + 0.5) / mult end
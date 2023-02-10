import math
import config
import lists

Seed = 937162211


def rint(lo=0, hi=1):  # n ; a integer lo..hi-1
    return math.floor(0.5 + rand(lo, hi))


def rand(lo=0, hi=1):  # n; a float "x" lo<=x < x
    global Seed
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rnd(n, nPlaces=3):  # num. return `n` rounded to `nPlaces`
    mult = 10 ** nPlaces
    return math.floor(n * mult + 0.5) / mult


def cosine(a, b, c):
    # find the x from line connecting a to b
    x1 = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x2 = max(0, min(1, x1))  # x2 is x1 confined between 0 and 1
    y = (a ** 2 - x2 ** 2) ** 0.5  # find the y from line connecting a to b
    return x2, y


# -- Non-parametric effect-size test
# --  M.Hess, J.Kromrey.
# --  Robust Confidence Intervals for Effect Sizes:
#     --  A Comparative Study of Cohen's d and Cliff's Delta Under Non-normality and Heterogeneous Variances
# --  American Educational Research Association, San Diego, April 12 - 16, 2004
# --  0.147=  small, 0.33 =  medium, 0.474 = large; med --> small at .2385
def cliffsDelta(ns1, ns2):
    if len(ns1) > 256:
        ns1 = lists.many(ns1, 256)
    if len(ns2) > 256:
        ns2 = lists.many(ns2, 256)
    if len(ns1) > 10 * len(ns2):
        ns1 = lists.many(ns1, 10 * len(ns2))
    if len(ns2) > 10 * len(ns1):
        ns1 = lists.many(ns2, 10 * len(ns1))
    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
    return abs(lt - gt) / n > config.the['cliffs']

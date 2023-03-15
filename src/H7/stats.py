import math
import random
import config

def samples(t, n):
    u = []
    for i in range(n):
        idx = random.randint(1, len(t)) - 1
        u.append(t[idx])
    return u

def cliffsDelta(ns1, ns2):
    n, gt, lt = 0, 0, 0
    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
    return math.abs(lt - gt) / n <= config.the['cliff']

def add(i, x):
    i['n'] += 1
    d = x - i['mu']
    i['mu'] += d / i['n']
    i['m2'] += d * (x - i['mu'])
    i['sd'] = 0 if i['n'] < 2 else (i['m2'] / (i['n'] - 1)) ** 0.5


def NUM(t=[]):
    i = {'n': 0, 'mu': 0, 'm2': 0, 'sd': 0}
    for x in t:
        add(i, x)
    return i


# n; return a sample from a Gaussian with mean `mu` and sd `sd`
def gaussian(mu=0, sd=1):
    return mu + sd * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())


def delta(i, other):
    e, y, z = 1E-32, i, other
    numerator = abs(y['mu'] - z['mu'])
    denominator = (e + (y['sd'] ** 2 / y['n']) + (z['sd'] ** 2 / z['n'])) ** 0.5

    return numerator / denominator


def RX(t, s):
    t.sort()
    return {'name': s or "", 'rank': 0, 'n': len(t), 'show': "", 'has': t}


def mid(t):
    t = t.has if hasattr(t, 'has') else t
    n = len(t) // 2
    if len(t) % 2 == 0:
        return (t[n - 1] + t[n]) / 2
    else:
        return t[n]


def div(t):
    t = t.has if hasattr(t, 'has') else t
    n = len(t)
    return (t[int(n * 9 / 10) - 1] - t[int(n * 1 / 10) - 1]) / 2.56


def merge(rx1, rx2):
    rx3 = RX([], rx1['name'])
    for x in rx1['has']:
        rx3['has'].append(x)

    for x in rx2['has']:
        rx3['has'].append(x)
    rx3['has'].sort()
    rx3['n'] = len(rx3['has'])
    return rx3


def tiles(rxs):
    huge = float('inf')
    lo, hi = huge, -huge
    for rx in rxs:
        lo = min(lo, rx['has'][0])
        hi = max(hi, rx['has'][-1])

    for rx in rxs:
        t = rx['has']
        u = [' ' for _ in range(config.the['width'])]

        def of(x, most):
            return max(1, min(most, x))

        def at(x):
            return t[of(len(t) * x // 1, len(t))]

        def pos(x):
            return math.floor(of(config.the['width'] * (x - lo) / (hi - lo + 1e-32) // 1, config.the['width']))

        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B + 1):
            u[i] = '-'
        for i in range(D, E + 1):
            u[i] = '-'
        u[config.the['width'] // 2] = '|'
        u[C] = '*'

        rx['show'] = ''.join(u) + ' {' + config.the['fmt'].format(a)
        for x in [b, c, d, e]:
            rx['show'] += ', ' + config.the['fmt'].format(x)
        rx['show'] += '}'

    return rxs
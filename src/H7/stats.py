import math
import random
import config


def samples(t, n=None):
    u = []
    n = n or len(t)
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
    return abs(lt - gt) / n <= config.the['cliff']


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
    denominator = (e + (y['sd'] ** 2 / y['n']) +
                   (z['sd'] ** 2 / z['n'])) ** 0.5

    return numerator / denominator


def RX(t, s):
    t.sort()
    return {'name': s or "", 'rank': 0, 'n': len(t), 'show': "", 'has': t}


def mid(t):
    if 'has' in t:
        t = t['has']
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
            # 0.1 -> 100 (-1?)
            return t[int(of(len(t) * x // 1, len(t)))-1]

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


def bootstrap(y0, z0):
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
    for y1 in y0:
        add(x, y1)
        add(y, y1)
    for z1 in z0:
        add(x, z1)
        add(z, z1)
    xmu, ymu, zmu = x['mu'], y['mu'], z['mu']
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for _ in range(1, config.the['bootstrap'] + 1):
        if delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs:
            n = n + 1
    return n / config.the['bootstrap'] >= config.the['conf']


def scottKnot(rxs, cohen):

    def merges(i, j):
        out = RX([], rxs[i]['name'])
        for k in range(i, j+1):
            out = merge(out, rxs[j])
        return out

    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut+1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])

    def recurse(lo, hi, rank):
        cut, best, l, l1, r, r1, now, b4 = None, 0, None, None, None, None, None, None
        b4 = merges(lo, hi)
        for j in range(lo, hi+1):
            if j < hi:
                l = merges(lo, j)
                r = merges(j+1, hi)
                now = (l['n'] * (mid(l) - mid(b4))**2 + r['n'] *
                       (mid(r) - mid(b4))**2) / (l['n'] + r['n'])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut+1, hi, rank)
        else:
            for i in range(lo, hi+1):
                rxs[i]['rank'] = rank
        return rank

    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(0, len(rxs)-1)) * config.the['cohen']
    recurse(0, len(rxs)-1, 1)
    return rxs

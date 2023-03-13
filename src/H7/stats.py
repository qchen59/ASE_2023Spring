import math
import random

import config

def samples(t,n):
    u = []
    for i in range(n):
        idx = random.randint(1,len(t))-1
        u.append(t[idx])
    return u

def add(i, x):
    i['n'] += 1
    d = x - i['mu']
    i['mu'] += d / i['n']
    i['m2'] += d * (x - i['mu'])
    i['sd'] = 0 if i['n'] < 2 else (i['m2'] / (i['n'] - 1)) ** 0.5

def NUM(t=[]):
    i = {'n': 0, 'mu': 0, 'm2': 0, 'sd': 0}
    for x in t:
        add(i,x)
    return i

# n; return a sample from a Gaussian with mean `mu` and sd `sd`
def gaussian(mu=0,sd=1):
    return mu + sd * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())

def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / ((e + y.sd**2/y.n + z.sd**2/z.n)**0.5)

def samples(t, n=None):
    u = []
    for i in range(0, n or len(t)):
        u.append(random.choice(t))
    return u

def bootstrap(y0, z0):
    x, y, z, yhat, zhat = [], [], [], [], []
    for y1 in y0:
        x.append(y1)
        y.append(y1)
    for z1 in z0:
        x.append(z1)
        z.append(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)
    tobs = delta(NUM(y), NUM(z))
    n = 0
    for _ in range(1, config.the['bootstrap'] + 1):
        if delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs:
            n = n + 1
    return n / config.the['bootstrap'] >= config.the['conf']
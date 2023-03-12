import math
import random

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
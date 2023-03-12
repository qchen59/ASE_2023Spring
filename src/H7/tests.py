import random
from stats import samples, NUM, gaussian

def ok(n=1):
    random.seed(1)

def sampleTest():
    ok()
    for i in range(10):
        print("",samples(["a","b","c","d","e"], 5))
    return True

def numTest():
    n = NUM([1,2,3,4,5,6,7,8,9,10])
    print("",n['n'],n['mu'],n['sd'])
    return True

def guassTest():
    ok()
    t = []
    for i in range(10**4):
        t.append(gaussian(10,2))
    n=NUM(t)
    print("",n['n'],n['mu'],n['sd'])
    return True

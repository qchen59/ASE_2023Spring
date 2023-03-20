import random
from stats import samples, NUM, gaussian, cliffsDelta, bootstrap, scottKnot, RX, tiles, mid
import numpy as np

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

def bootmuTest():
    ok()
    a = [gaussian(10,1) for i in range(100)]
    print("mu\tsd\tcliffs\tboot\tboth")
    print("--\t--\t------\t----\t----")
    for mu in np.arange(10, 11, 0.1):
        b = [gaussian(mu,1) for i in range(100)]
        cl = cliffsDelta(a, b)
        bs = bootstrap(a, b)
        print(round(mu,2),"\t",1,"\t",cl,"\t",bs,"\t",cl and bs)
    return True

def basicTest():
    ok()
    print("\t\tTrue", bootstrap( [8, 7, 6, 2, 5, 8, 7, 3],[8, 7, 6, 2, 5, 8, 7, 3]),cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3],[8, 7, 6, 2, 5, 8, 7, 3]))
    print("\t\tFalse", bootstrap(  [8, 7, 6, 2, 5, 8, 7, 3],[9, 9, 7, 8, 10, 9, 6]),cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3],[9, 9, 7, 8, 10, 9, 6]))
    print("\t\tFalse", bootstrap([0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6],[0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9]),cliffsDelta([0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6],[0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9]))
    return True

def preTest():
    ok()
    print("\neg3")
    d = 1
    for i in range(10):
        t1, t2 = [], []
        for j in range(32):
            t1.append(gaussian(10, 1))
            t2.append(gaussian(d * 10, 1))
        print(f"\t{d}, {d < 1.1}, {bootstrap(t1, t2)}, {bootstrap(t1, t1)}")
        d += 0.05
    return True

def fiveTest():
    ot = scottKnot([
        RX([0.34,0.49,0.51,0.6,.34,.49,.51,.6],"rx1"),
        RX([0.6,0.7,0.8,0.9,.6,.7,.8,.9],"rx2"),
        RX([0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35],"rx3"),
        RX([0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9],"rx4"),
        RX([0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4],"rx5")])
    o = tiles(ot)
    for rx in o:
        print(rx['name'],rx['rank'],rx['show'])
    return True

def sixTest():
    ok()
    o = tiles(scottKnot([
                  RX([101,100,99,101,99.5,101,100,99,101,99.5],"rx1"),
                  RX([101,100,99,101,100,101,100,99,101,100],"rx2"),
                  RX([101,100,99.5,101,99,101,100,99.5,101,99],"rx3"),
                  RX([101,100,99,101,100,101,100,99,101,100],"rx4")]))
    for rx in o:
        print(rx['name'],rx['rank'],rx['show'])
    return True

def tilesTest():
    ok()
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    for i in range(1000):
        a.append(gaussian(10, 1))
    for i in range(1000):
        b.append(gaussian(10.1, 1))
    for i in range(1000):
        c.append(gaussian(20, 1))
    for i in range(1000):
        d.append(gaussian(30, 1))
    for i in range(1000):
        e.append(gaussian(30.1, 1))
    for i in range(1000):
        f.append(gaussian(10, 1))
    for i in range(1000):
        g.append(gaussian(10, 1))
    for i in range(1000):
        h.append(gaussian(40, 1))
    for i in range(1000):
        j.append(gaussian(40, 3))
    for i in range(1000):
        k.append(gaussian(10, 1))
    for i,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
        rxs.append(RX(v, "rx"+str(i)))
    rxs.sort(key=lambda x: mid(x))
    for rx in tiles(rxs):
        print("", rx['name'], rx['show'])
    return True

def skTest():
    ok()
    rxs, a, b, c, d, e, f, g, h, j, k = [], [], [], [], [], [], [], [], [], [], []
    for i in range(1000):
        a.append(gaussian(10, 1))
    for i in range(1000):
        b.append(gaussian(10.1, 1))
    for i in range(1000):
        c.append(gaussian(20, 1))
    for i in range(1000):
        d.append(gaussian(30, 1))
    for i in range(1000):
        e.append(gaussian(30.1, 1))
    for i in range(1000):
        f.append(gaussian(10, 1))
    for i in range(1000):
        g.append(gaussian(10, 1))
    for i in range(1000):
        h.append(gaussian(40, 1))
    for i in range(1000):
        j.append(gaussian(40, 3))
    for i in range(1000):
        k.append(gaussian(10, 1))
    for i,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
        rxs.append(RX(v, "rx"+str(i)))
    for rx in tiles(scottKnot(rxs)):
        print("", rx['name'], rx['show'])
    return True
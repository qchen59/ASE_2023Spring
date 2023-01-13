#script.lua -> script.py

# -- NUM
# -- Summarizes a stream of numbers.
class Num:
    def __init__(self):
        # number of numbers
        self.n = 0
        # mean
        self.mu = 0
        self.m2 = 0
        # the smallest number
        self.lo = float('inf')
        # largest number
        self.hi = float('-inf')
    # add `n`, update lo,hi and stuff needed for standard deviation
    def add(self, n):
        if n != "?":
            # add one more number
            self.n += 1
            # difference = new adding number - mean of number stream
            d = n - self.mu
            # update the new mean
            self.mu += d/self.n
            # For stand deviation
            self.m2 += d*(n-self.mu)
            # Update the smallest
            self.lo = min(n, self.lo)
            # Update the largest
            self.hi = max(n, self.hi)

    # return mean
    def mid(self):
        return self.mu

    # return standard deviation using Welford's algorithm http://t.ly/nn_W
    def div(self):
        return (self.m2 < 0 or self.n < 2) and 0 or pow(self.m2/(self.n-1), 0.5)


# function NUM.new(i) --> NUM;  constructor;
# i.n, i.mu, i.m2 = 0, 0, 0
# i.lo, i.hi = math.huge, -math.huge end
#
# function NUM.add(i,n) --> NUM; add `n`, update lo,hi and stuff needed for standard deviation
#     if n ~= "?" then
#     i.n  = i.n + 1
#     local d = n - i.mu
#     i.mu = i.mu + d/i.n
#     i.m2 = i.m2 + d*(n - i.mu)
#     i.lo = math.min(n, i.lo)
#     i.hi = math.max(n, i.hi) end end
#
# function NUM.mid(i,x) return i.mu end --> n; return mean
# function NUM.div(i,x)  --> n; return standard deviation using Welford's algorithm http://t.ly/nn_W
# return (i.m2 <0 or i.n < 2) and 0 or (i.m2/(i.n-1))^0.5  end
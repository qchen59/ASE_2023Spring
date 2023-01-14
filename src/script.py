#script.lua -> script.py
import math
import re

class Num:
    def __init__(self) -> None:
        self.n = 0
        self.has = {}
        self.most, self.mode = 0,None

    def add(self, x):
        if x != "?": 
            self.n = self.n + 1 
            self.has[x] = 1 + (self.has[x] or 0)
            if self.has[x] > self.most:
                self.most,self.mode = self.has[x], x

    def mid(self, x):
        return self.mode
    
    def div(self, x, fun, e):
        def fun(p):
            return p*math.log(p,2)
        
        e = 0
        for _,n in enumerate(self.has):
            e += fun(n/self.n)
        
        return -e
    

# Strings
def coerce(s:str):
    try:
        if s.lower()=='true':
            return True
        elif s.lower()=='false':
            return False
        try:
            return int(s)
        except Exception as e:
            try:
                return int(s)
            except Exception as e:
                try:
                    return float(s)
                except Exception as e:
                    return s.strip()
    except Exception as e:
        return s
    


# Main
# def settings(s, t):
#     t = {}
#     re.sub(r'\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)',)

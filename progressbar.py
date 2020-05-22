import time
import sys
import math


def as_minutes(s):
    """Formats seconds to min sec."""
    m = math.floor(s / 60)
    s -= m * 60
    return "{:d}m {:4.1f}s".format(m, s)


class ProgBar:
    def __init__(self, size, name="", barwidth=40):
        self.size = size
        self.barwidth = barwidth
        self. name = "" if name.strip() == "" else name + " "
        self.idx = 0
        self.strsize = 0
        self.start = time.time()

    def step(self, nb, vals=None):
        if self.idx < self.size:
            self.idx += nb
            self.show(vals)
            # new line if end of progress
            if self.idx == self.size: print("")

    def evolution(self):
        perc = self.idx / self.size
        return "[{}{:5.1f}%]".format(self.name, 100*perc)

    def stats(self, vals=None):
        now = time.time()
        perc = self.idx / self.size
        s = now - self.start
        es = s / perc
        rs = es - s
        ts = "time: {}|rem: {}".format(as_minutes(s), as_minutes(rs))
        valstr = ""
        if vals is not None:
            for key, val in vals.items():
                valstr += "{}: {}|".format(key, val)

        return "[{}{}]".format(valstr, ts)
    
    def progressbar(self):
        perc = self.idx / self.size
        r = int(1000*perc) % 10
        n = self.idx*self.barwidth//self.size
        m = self.barwidth - n
        s = ""
        if r != 0: 
            m -= 1 
            s = str(r)
        n = "#"*n
        m = " "*m
        return "[{}]".format(n+s+m)
    
    def show(self, vals=None):
        perc = (self.idx)/self.size
        msg = self.evolution() + self.progressbar() + self.stats(vals)
        d = len(msg)
        if d >= self.strsize:
            n, self.strsize = 0, d

        else:
            n = self.strsize - d
        msg += " "*n
        print(msg, end='\r', flush=True)
    
    def reset(self):
        self.idx = 0
        self.strsize = 0
        self.start = time.time()
    
    def close(self):
        if self.idx != self.size: print("")


if __name__ == "__main__":
    pbar = ProgBar(125)
    for i in range(125):
        pbar.step(1, vals={'step': i+1, 'total': 125})
        time.sleep(0.1)

import math
def bernstein(i, m, t) -> float:
    return math.comb(m, i) * (t ** i) * ((1 - t) ** (m - i))
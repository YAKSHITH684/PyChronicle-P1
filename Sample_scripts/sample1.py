count: int = 0
name = "pychronicle"

def compute(a, b):
    total = a + b
    total += 1
    return total

class Config:
    debug = True
    x: int = 1
    y: int = 2
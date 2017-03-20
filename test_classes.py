class MyBinary:
    width = 0
    bits = []
    def __init__(self, width = 0, bits = []):
        self.width = width
        self.bits = bits

class SBinary:
    sgn = 0
    bnry = MyBinary()
    def __init__(self, sgn = 0, bnry = MyBinary()):
        self.sgn = sgn
        self.bnry = bnry

class MyFloat:
    exp = SBinary()
    num = SBinary()
    def __init__(self, exp = SBinary(0, MyBinary(5, [0])), num = SBinary(0, MyBinary(10, [1, 2, 3]))):
        self.exp = exp
        self.num = num

    def __add__(self, other):
        return [self, other]

x = MyFloat()
#y = MyFloat(SBinary(1, MyBinary(9, [0, 3])), SBinary(1, MyBinary(2, [1, 2, 2, 3])))
y = MyFloat()

[x_a, y_a] = x + y

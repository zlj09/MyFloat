import math

exp_width = 15;
num_width = 15;

class MyBinary:
    width = 0;
    bits = []

    def __init__(self, width = 0, bits = []):
        self.width = width
        self.bits = bits
    
    def set(self, width, value):
        self.width = width
        self.bits = [0] * width
        val = int(value)
        for i in range(0, width):
            if val != 0:
                [val, b] = divmod(val, 2)
                self.bits[i] = b    
            else:
                self.bits[i] = 0

    def getBit(self, i):
        if (i < self.width):
            return self.bits[i]
        else:
            return 0
                    
    def __add__(self, other):
        width = max(self.width, other.width)
        res = MyBinary()
        res.width = width
        res.bits = [0] * width
        c = 0
        for i in range(0, width):
            a = self.getBit(i)
            b = other.getBit(i)
            res.bits[i] = a ^ b ^ c
            c = (a & c) | (b & c) | (a & b)
        if c == 1:
            res.width = res.width + 1
            res.bits = res.bits + [1]
        return res

    def __sub__(self, other):
        width = max(self.width, other.width)
        res = MyBinary()
        res.width = width
        res.bits = [0] * width
        c = 0
        for i in range(0, width):
            a = self.getBit(i)
            b = other.getBit(i)
            res.bits[i] = a ^ b ^ c
            c = ~a & ~b & c | ~a & b & ~c | ~a & b & c | a & b & c
        return res

    def __lshift__(self, n):
        res = MyBinary()
        res.width = self.width + n
        res.bits = [0] * n + self.bits
        return res

    def __rshift__(self, n):
        res = MyBinary()
        res.width = self.width - n
        res.bits = self.bits[n : len(self.bits)]
        return res
        
    
    def __mul__(self, other):
        res = MyBinary()        
        res.width = self.width + other.width
        res.bits = [0] * res.width

        for i in range(0, self.width):
            if self.bits[i] == 1:
                res = res + (other << i)
        return res

    def __lt__(self, other):
        width = max(self.width, other.width)
        i = width - 1;
        while(i >= 0):
            if (self.getBit(i) < other.getBit(i)):
                return True
            if (self.getBit(i) > other.getBit(i)):
                return False
            i = i - 1
        return False

    def __str__(self):
        bin_str = 'width:' + str(self.width) + '\t' + 'bits: ' + str(self.bits)
        return(bin_str)

    def toDec(self):
        bit_list = ['0'] * self.width
        for i in range(0, self.width):
            bit_list[i] = str(self.bits[i])
        bit_list.reverse()
        bit_str = ''.join(bit_list)

        if bit_str == '':
            return 0
        else:
            return(int(bit_str, 2))

    def trounding(self, trnd_width):
        if self.width <= trnd_width:
            return self
        else:
            self.width = trnd_width

            lsb = self.bits[-trnd_width] | self.bits[-trnd_width]
            self.bits = self.bits[-trnd_width : len(self.bits)]
            self.bits[0] = lsb
            return self

class SBinary:
    sgn = 0
    bnry = MyBinary()

    def __init__(self, sgn = 0, bnry = MyBinary()):
        self.sgn = sgn
        self.bnry = bnry

    def set(self, sgn, width, value):
        self.sgn = sgn
        self.bnry.set(width, value)

    def __lt__(self, other):
        if self.sgn == 0 and other.sgn == 0:
            if self.bnry < other.bnry:
                return True
            else:
                return False
        if self.sgn == 1 and other.sgn == 0:
            return True
        if self.sgn == 0 and other.sgn == 1:
            return False
        if self.sgn == 1 and other.sgn == 1:
            if self.bnry < other.bnry:
                return False
            else:
                return True

    def __lshift__(self, n):
        res = SBinary()
        res.sgn = self.sgn
        res.bnry = self.bnry << n
        return res

    def __add__(self, other):
        res = SBinary()
        if (self.sgn == 0 and other.sgn == 0):
            res.sgn == 0
            res.bnry = self.bnry + other.bnry
        if (self.sgn == 0 and other.sgn == 1):
            if (self.bnry < other.bnry):
                res.sgn = 1
                res.bnry = other.bnry - self.bnry
            else:
                res.sgn = 0
                res.bnry = self.bnry - other.bnry
        if (self.sgn == 1 and other.sgn == 0):
            if (self.bnry < other.bnry):
                res.sgn = 0
                res.bnry = other.bnry - self.bnry
            else:
                res.sgn = 1
                res.bnry = self.bnry - other.bnry
        if (self.sgn == 1 and other.sgn == 1):
            res.sgn = 1
            res.bnry = self.bnry + other.bnry
        return res

    def __sub__(self, other):
        if other.sgn == 0:
            other.sgn = 1
        else:
            other.sgn = 0
        return self + other

    def __str__(self):
        sb_str = 'sign: ' + str(self.sgn) + '\t' + 'binary: ' + str(self.bnry)
        return sb_str

    def toDec(self):
        if (self.sgn == 0):
            return self.bnry.toDec()
        else:
            return -self.bnry.toDec()

    def trounding(self, trnd_width):        
        self.bnry.trounding(trnd_width)

class MyFloat:
    exp = SBinary()
    num = SBinary()

    def __init__(self, exp = SBinary(1, MyBinary(5, [0])), num = SBinary(0, MyBinary(3, [1, 2, 3]))):
        self.exp = exp
        self.num = num

    def set(self, s):
        x = float(s)
        if x < 0:
            nsgn = 1
            x = abs(x)
        else:
            nsgn = 0

        b = int(math.log(x) / math.log(2)) + 1
        a = x * (pow(2, (exp_width - b)))
        if b < 0:
            esgn = 1
            b = abs(b)
        else:
            esgn = 0
          
        self.exp.set(esgn, exp_width, b)
        self.num.set(nsgn, num_width, a)
        
    def __add__(self, other):
        if self.exp < other.exp:
            flarge = other
            fsmall = self
        else:
            flarge = self
            fsmall = other

        exp = fsmall.exp
        num = flarge.num << (flarge.exp.toDec() - fsmall.exp.toDec())
        num = num + fsmall.num

        extra_exp = SBinary()
        extra_exp.set(0, num_width, num.bnry.width - num_width)
        exp = exp + extra_exp

        num.trounding(num_width)

        res = MyFloat(exp, num)
        return res
        
    def __sub__(self, other):
        if other.num.sgn == 0:
            other.num.sgn = 1
        else:
            other.num.sgn = 0
        return self + other

    def __str__(self):
        flt_str = 'exp: ' + str(self.exp) + '\n' + 'num: ' + str(self.num)
        return(flt_str)

    def toFloat(self):
        exp = self.exp.toDec()
        num = self.num.toDec()
        return num / pow(2, (exp_width - exp))
    

    
        

##s = '-0.125'
##f = MyFloat()
##f.set(s)
##print(f.exp.bits, f.num.bits)
        
##a = MyBinary()
##a.set(9, 240)
##b = MyBinary()
##b.set(4, 15)
##c = a + b
##print(c.bits)

##a = MyBinary()
##a.set(4, 13)
##a = a << 2
##print(a)

##a = MyBinary()
##a.set(4, 5)
##b = MyBinary()
##b.set(4, 7)
##c = a * b
##print(c)

##print(x)
##print(x.toFloat())
##print(y)
##print(y.toFloat())
##print(x, '\n', y)

##[x_a, y_a] = x + y
##print(x, '\n', y)
##print(x_a, '\n', y_a)

##a = MyBinary()
##a.set(8, 1)
##b = MyBinary()
##b.set(5, 25)
##print(a < b)

##a = MyBinary()
##a.set(16, 456)
##print(a)
##print(a.toDec())


x = MyFloat()
x.set(300)
y = MyFloat(SBinary(1, MyBinary(9, [0, 3])), SBinary(1, MyBinary(2, [1, 2, 2, 3])))
y.set(-5)
z = x - y
print(z)
print(z.toFloat())

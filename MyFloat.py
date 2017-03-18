import math

exp_width = 15;
num_width = 15;

class MyBinary:
    width = 0;
    bits = []
    
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
        return res

    def __sub__(self, other):
        width = max(self.width, other.width)
        res = MyBinary()
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
    
    def __mul__(self, other):
        res = MyBinary()        
        res.width = self.width + other.width
        res.bits = [0] * res.width

        print(self, other)

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
        bin_str = 'width:' + str(self.width) + ' ' + 'bits: ' + str(self.bits)
        return(bin_str)

    def toDec(self):
        bit_list = ['0'] * self.width
        for i in range(0, self.width):
            bit_list[i] = str(self.bits[i])
        bit_list.reverse()
        bit_str = ''.join(bit_list)
        return(int(bit_str, 2))        

class MyFloat:
    esgn = 0;
    exp = MyBinary()
    nsgn = 0;
    num = MyBinary()

    def set(self, s):
        x = float(s)
        if x < 0:
            self.nsgn = 1
            x = abs(x)
        b = int(math.log(x) / math.log(2)) + 1
        a = x * (pow(2, (exp_width - b)))
        if b < 0:
            self.esgn = 1
            b = abs(b)
        self.exp.set(exp_width, b)
        self.num.set(num_width, a)

    def __add__(self, other):
        res = MyFloat()
        

    def __str__(self):
        flt_str = "exp sign: " + str(self.esgn) + " exp:" + str(self.exp) + " num sign:" + str(self.nsgn) + " num: " + str(self.num)
        return(flt_str)

    def toFloat(self):
        if self.esgn == 0:
            exp = self.exp.toDec()
        else:
            exp = -self.exp.toDec()

        if self.nsgn == 0:
            num = self.num.toDec()
        else:
            num = -self.num.toDec()

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

x = MyFloat()
x.set(0.00078)
y = MyFloat()
y.set(0.01078)

a = MyBinary()
a.set(8, 1)
b = MyBinary()
b.set(5, 25)

print(a < b)
print(x.toFloat())

##a = MyBinary()
##a.set(16, 456)
##print(a)
##print(a.toDec())

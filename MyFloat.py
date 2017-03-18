import math

index_width = 15;
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
    

class MyFloat:
    isgn = 0;
    index = MyBinary()
    nsgn = 0;
    num = MyBinary()

    def set(self, s):
        x = float(s)
        if x < 0:
            self.nsgn = 1
            x = abs(x)
        b = int(math.log(x) / math.log(2)) + 1
        a = x * (1 << (index_width - b))
        if b < 0:
            self.isgn = 1
            b = abs(b)
        self.index.set(index_width, b)
        self.num.set(num_width, a)

    
        

s = '-0.125'
f = MyFloat()
f.set(s)
print(f.index.bits, f.num.bits)
b = MyBinary()
b.set(4, 15)

            

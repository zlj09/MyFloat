#!/usr/bin/python3 
# -*- coding: utf-8 -*-


import math

##参考讲义，定义32位浮点数的阶符为1位，阶码为15位，数符为1位，数码为15位
exp_width = 15;
num_width = 15;


## MyBinary -- 无符号二进制数类
class MyBinary:
    width = 0;
    bits = []

    def __init__(self, width = 0, bits = []):
        self.width = width
        self.bits = bits
    
##    根据位宽和十进制数值生成无符号二进制数
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

##    无符号二进制加法器，可能产生进位                 
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

##    无符号二进制减法器，不产生借位，需要先比较操作数大小，保证够减
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

##    无符号二进制乘法器，结果经过化简，去掉多余的0
    def __mul__(self, other):
        res = MyBinary()        
        res.width = 1
        res.bits = [0]

        other.simplify()

        for i in range(0, self.width):
            if self.bits[i] == 1:
                res = res + (other << i)
        return res

##    无符号二进制乘法器，结果经过化简
    def __truediv__(self, other):
        res = MyBinary()
        res.width = num_width
        res.bits = [0] * num_width

        if (self < other):
            self = self << 1

        i = num_width - 1
        while(i >= 0):
            if (self < other):
                res.bits[i] = 0
            else:
                res.bits[i] = 1
                self = self - other
            i = i - 1
            self = self << 1

        res.simplify()

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

##    无符号二进制到十进制的转化函数，利用Python格式转化函数实现，用于检验结果和Debug
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

##    舍入函数，参考讲义，采用截取和舍入相结合的方式
    def trounding(self, trnd_width):
        if self.width <= trnd_width:
            return self
        else:
            self.width = trnd_width

            lsb = self.bits[-trnd_width] | self.bits[-trnd_width]
            self.bits = self.bits[-trnd_width : len(self.bits)]
            self.bits[0] = lsb
            return self
        
##    化简函数，去掉开头多余的0
    def simplify(self):
        while(1):
            if (self.bits[-1] == 0):
                self.width = self.width - 1
                del(self.bits[-1])
            else:
                break
            if (self.width == 0):
                break


## SBinary -- 有符号二进制数类
class SBinary:
##    由1位符号位和无符号二进制数构成
    sgn = 0
    bnry = MyBinary()

    def __init__(self, sgn = 0, bnry = MyBinary()):
        self.sgn = sgn
        self.bnry = bnry

##    由符号，位宽和十进制数值生成有符号二进制数
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

##    有符号二进制数加法，判断符号，比较大小，再调用合适的无符号二进制运算函数实现
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

    def __mul__(self, other):
        res = SBinary()
        res.sgn = self.sgn ^ other.sgn
        res.bnry = self.bnry * other.bnry
        return res

    def __truediv__(self, other):
        res = SBinary()
        res.sgn = self.sgn ^ other.sgn
        res.bnry = self.bnry / other.bnry
        return res

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

        
## MyFloat -- 自定义32位浮点数类
class MyFloat:
##    由阶符，阶码，数符和数码构成（阶符和数符隐藏在SBinary类中）
    exp = SBinary()
    num = SBinary()

    def __init__(self, exp = SBinary(1, MyBinary(5, [0])), num = SBinary(0, MyBinary(3, [1, 2, 3]))):
        self.exp = exp
        self.num = num

##    由字符串生成自定义浮点数（借用了一些float运算函数）
    def set(self, s):
        x = float(s)
        if x < 0:
            nsgn = 1
            x = abs(x)
        else:
            nsgn = 0
            
        if x == 0:
            b = 0
        else:
            b = int(math.log(x) / math.log(2)) + 1
            
        a = x * (pow(2, (exp_width - b)))
        if b < 0:
            esgn = 1
            b = abs(b)
        else:
            esgn = 0
          
        self.exp.set(esgn, exp_width, b)
        self.num.set(nsgn, num_width, a)

##    自定义浮点数加法
    def __add__(self, other):
##        比较阶码，完成对阶
        if self.exp < other.exp:
            flarge = other
            fsmall = self
        else:
            flarge = self
            fsmall = other
        exp = fsmall.exp

##        尾数加操作
        num = flarge.num << (flarge.exp.toDec() - fsmall.exp.toDec())
        num = num + fsmall.num
        
##        结果规格化
        extra_exp = SBinary()
        extra_exp.set(0, exp_width, num.bnry.width - num_width)
        exp = exp + extra_exp
        
##        舍入处理
        num.trounding(num_width)

        res = MyFloat(exp, num)
        return res
    
##    自定义浮点数减法，改变减数符号，调用加法实现    
    def __sub__(self, other):
        if other.num.sgn == 0:
            other.num.sgn = 1
        else:
            other.num.sgn = 0
        return self + other
    
##    自定义浮点数乘法
    def __mul__(self, other):
##        阶码加操作
        exp = self.exp + other.exp

##        尾数乘操作
        num = self.num * other.num

##        结果规格化
        dropped_exp = SBinary()
        dropped_exp.set(0, exp_width, 2 * num_width - num.bnry.width)
        exp = exp - dropped_exp

##        舍入处理
        num.trounding(num_width)
        
        res = MyFloat(exp, num)
        return res

##    自定义浮点数除法
    def __truediv__(self, other):
##        零操作数检查
        if 1 not in other.num.bnry.bits:
            raise ZeroDivisionError
        
        
##        阶码减操作
        exp = self.exp - other.exp

##        尾数除操作
        num = self.num / other.num

##        结果规格化
        if (self.num.bnry < other.num.bnry):
            exp
        else:
            extra_exp = SBinary()
            extra_exp.set(0, exp_width, 1)
            exp = exp + extra_exp

        res = MyFloat(exp, num)
        return res

    def __str__(self):
        flt_str = 'exp: ' + str(self.exp) + '\n' + 'num: ' + str(self.num)
        return(flt_str)

##    自定义浮点数类型到标准浮点数类型的转换函数，只用于输出和对比结果
    def toFloat(self):
        exp = self.exp.toDec()
        num = self.num.toDec()
        return num / pow(2, (exp_width - exp))



##测试程序
##实例化MyFloat对象（为了防止内存重叠，进行了较为复杂的初始化）
mf0 = MyFloat()
mf1 = MyFloat(SBinary(1, MyBinary(9, [0, 3])), SBinary(1, MyBinary(2, [1, 2, 2, 3])))

##测试用例
test_len = 10
test_list = \
          [[4.0,  0, 2342.457,      -0.25,  -256.834,   4.5e8,  7.7e-3,  5.5e150,     5.5e160,  15.0],\
           [6.0,  20.0, -1785.128,  86.78,  -3233.1982, -2.4e6, 3.9e-5,  -4.9e153,    -4.9e163, 0.0]]

##测试过程
for i in range(0, test_len):
    f0 = test_list[0][i]
    f1 = test_list[1][i]

    print('Test Cast ', i, ': ', f0, '\t', f1)

    f_res = f0 + f1
    mf0.set(f0)
    mf1.set(f1)
    mf_res = mf0 + mf1
    print('Add:\t', f_res, '\t', mf_res.toFloat(), '\t')

    f_res = f0 - f1
    mf0.set(f0)
    mf1.set(f1)
    mf_res = mf0 - mf1
    print('Sub:\t', f_res, '\t', mf_res.toFloat(), '\t')

    f_res = f0 * f1
    mf0.set(f0)
    mf1.set(f1)
    mf_res = mf0 * mf1
    print('Mul:\t', f_res, '\t', mf_res.toFloat(), '\t')

    try:
        f_res = f0 / f1
        mf0.set(f0)
        mf1.set(f1)
        mf_res = mf0 / mf1
        print('Div:\t', f_res, '\t', mf_res.toFloat(), '\t')
    except ZeroDivisionError:
        print('Error: Divided by Zero')

    print('\n')
    

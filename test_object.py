class A:
    atr1 = 0

class B:
    a1 = A()
    a2 = A()

def swp(a, b):
    t = a
    a = b
    b = t

b = B
b.a1.atr1 = 5

print(b.a2.atr1)

c = b
print(c.a1.atr1)
c.a1.atr1 = 10
print(c.a1.atr1)
print(b.a1.atr1)

a = 5
b = 3
swp(a,b)
print(a)
print(b)

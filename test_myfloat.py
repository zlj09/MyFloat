import MyFloat

mf0 = MyFloat.MyFloat()
mf1 = MyFloat.MyFloat(MyFloat.SBinary(1, MyFloat.MyBinary(9, [0, 3])), MyFloat.SBinary(1, MyFloat.MyBinary(2, [1, 2, 2, 3])))

##测试用例
test_len = 10
test_list = \
          [[4.0,  0, 2342.457,      -0.25,  -256.834,   4.5e8,  7.7e-3,  5.5e150,     5.5e160,  15.0],\
           [6.0,  20.0, -1785.128,  86.78,  -3233.1982, -2.4e6, 3.9e-5,  -4.9e153,    -4.9e163, 0.0]]

##测试过程
for i in range(0, test_len):
    f0 = test_list[0][i]
    f1 = test_list[1][i]

##    print(f0, '\t', f1)
##
##    f_res = f0 + f1
##    mf0.set(f0)
##    mf1.set(f1)
##    mf_res = mf0 + mf1
##    print(f_res, '\t', mf_res.toFloat(), '\t')
##
##    f_res = f0 - f1
##    mf0.set(f0)
##    mf1.set(f1)
##    mf_res = mf0 - mf1
##    print(f_res, '\t', mf_res.toFloat(), '\t')
##
##    f_res = f0 * f1
##    mf0.set(f0)
##    mf1.set(f1)
##    mf_res = mf0 * mf1
##    print(f_res, '\t', mf_res.toFloat(), '\t')
##
    try:
        f_res = f0 / f1
        mf0.set(f0)
        mf1.set(f1)
        mf_res = mf0 / mf1
        print(f_res, '\t', mf_res.toFloat(), '\t')
    except ZeroDivisionError:
        print('Error: Divided by Zero')


    

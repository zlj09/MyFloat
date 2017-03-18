index_bit = 15;
num_bit = 15;

class MyFloat:
    index_sign = 0
    index = [0] * index_bit
    num_sign = 0
    num = [0] * num_bit
    def __init__(self, s):
        if 'e' in s:
            [s_num, s_e, s_exp] = s.partition('e')
        else:
            if 'e' in s:
                [s_num, s_e, s_exp] = s.partition('e')
            else:
                s_num = s;
                s_exp = '0';
        if '.' in s_num:
            decimal = len(s_num) - (s_num.find('.') + 1)
            [s_int, s_p, s_dec] = s_num.partition('.')
            s_num = s_int + s_dec
        else:
            decimal = 0;
        num10 = int(s_num)
        exp10 = int(s_exp) - decimal;
            

s = '0.23e-2'
f = MyFloat(s)
            

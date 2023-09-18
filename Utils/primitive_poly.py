# -*- encoding: utf-8 -*-
'''
@File    :   primitive_poly.py
@Time    :   2023/03/05 19:44:11
@Author  :   zeroc 
'''
def add(x, y):
    """
    二进制加法 -> 异或
    """
    return x ^ y

def div(x, y):
    """
    实现有限域内多项式的除法
    """
    if len(bin(x)[2:]) < len(bin(y)[2:]):  #! 被除多项式次数小于除多项式
        return 0, x
    elif len(bin(x)[2:]) == len(bin(y)[2:]):
        return 1, x ^ y
    res = 0
    l = x.bit_length() - y.bit_length()
    while l >= 0:
        x ^= (y << l)  #! 逐位相减
        res ^= (1 << l)  #! 上商
        l = x.bit_length() - y.bit_length()
    return res, x

def mul(x, y):
    """
    实现有限域内多项式的乘法
    """
    if x == 0 or y == 0:  #! 乘数存在0
        return 0
    res = 0
    while y != 0:
        if y & 1 == 1:
            res ^= x
        x <<= 1
        x = div(x, 0x11b)[1]
        y >>= 1
    return res

def poly_exgcd(x, y):
    """
    实现有限域内多项式的欧几里得算法

    参数：
    x, y -> 输入的有限域元素

    返回值：
    x1, y1 -> 对应元素的系数
    m -> 最大公因式
    """
    if y == 0:  #! 存在元素0
        return 1, 0, x
    else:  #! 采用迭代法求gcd
        x1, y1, m = poly_exgcd(y, div(x, y)[1])
        x = y1
        y = x1 ^ mul(y1, div(x, y)[0])
        return x, y, m

def is_prime(x):
    """
    判断x所代表的的多项式是否为不可约多项式
    """
    n = len(bin(x)[2:])
    for i in range(1, 2 ** (n // 2 + 1)):
        if poly_exgcd(x, i)[2] != 1:
            return False
    return True

def is_primitive(x):
    """
    判断是否为本原多项式
    """
    n = len(bin(x)[2:])
    if not is_prime(x):  #! 是否为不可约多项式
        return False
    if poly_exgcd(x, 2 ** (2 ** (n - 1) - 1) + 1)[2] != x:  #! 是否整除x^m+1(m=2^n-1)
        return False
    for i in range(2 ** (n - 1) - 1):
        if poly_exgcd(x, 2 ** i + 1)[2] == x:  #! 是否整除x^q+1(q<m)
            return False
    return True


if __name__ == "__main__":
    for i in range(2 ** 8, 2 ** 9):
        if is_primitive(i):
            print(bin(i)[2:], end=" ")
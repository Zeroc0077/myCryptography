# -*- encoding: utf-8 -*-
'''
@File    :   CRT.py
@Time    :   2023/02/23 16:30:37
@Author  :   zeroc 
'''
from Utils.number import *


def CRT(a, b):
    """
    实现中国剩余定理

    参数：
    a -> 模数数组
    b -> 余数数组

    返回值：
    满足同余方程的最小正整数
    """
    if set(b) == {0}:  # ! 考虑余数全为0的情况
        res = a[0]
        for i in range(1, len(a)):
            res *= a[i] // Exgcd(res, a[i])[2]
        return res
    M = []
    M1 = []
    m = 1
    res = 0
    for i in a:
        m *= i  # ! 全部模数的乘积
    for i in a:
        M.append(m // i)
    for i, j in zip(M, a):
        M1.append(inverse(i, j))
    for i in range(len(a)):
        res += (b[i] % a[i]) * M[i] * M1[i]
    return res % m


if __name__ == "__main__":
    a1, a2, a3 = input().split()
    b1, b2, b3 = input().split()
    a1, a2, a3, b1, b2, b3 = int(a1), int(
        a2), int(a3), int(b1), int(b2), int(b3)
    a = [a1, a2, a3]
    b = [b1, b2, b3]
    print(CRT(a, b))

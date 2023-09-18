# -*- encoding: utf-8 -*-
'''
@File    :   Knownedn.py
@Time    :   2023/04/17 11:00:56
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from random import *
from Utils.utils import *


def FactorizeN(n, e, d):
    k = e * d - 1  # 求得φ(n)
    r = k
    t = 0
    y = 0
    success = False
    while True:  # 将φ(n)分解为2^t * r的形式
        r = r // 2
        t += 1
        if r % 2 == 1:
            break
    while not success:
        g = randint(0, n - 1)
        y = pow(g, r, n)
        if y == 1 or y == n - 1:  # g需要满足g^r != 1, -1 mod n
            continue
        for i in range(t):
            x = pow(y, 2, n)
            if x == 1 and Exgcd(y - 1, n)[2] > 1:  # 说明找到了一个公因子
                success = True
                break
            elif x == n - 1:
                continue
            else:
                y = x
    if success:
        p = Exgcd(y - 1, n)[2]
        q = n // p
        assert p * q == n
        return p, q
    else:
        print('Factorization Failed')


if __name__ == "__main__":
    e = int(input())
    d = int(input())
    n = int(input())
    p, q = FactorizeN(n, e, d)
    if p < q:
        p, q = q, p
    print(q)
    print(p)

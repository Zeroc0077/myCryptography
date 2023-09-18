# -*- encoding: utf-8 -*-
'''
@File    :   BBS.py
@Time    :   2023/04/04 22:26:24
@Author  :   zeroc 
'''
from random import randint


def BBS(seed, l, module):
    pre = seed ** 2 % module
    res = ""
    while len(res) < l:
        pre = pre ** 2 % module
        res += str(pre & 1)
    return res[::-1]


if __name__ == '__main__':
    l = int(input())
    # p = getPrime(1024)
    p = int(input())
    # q = getPrime(1024)
    q = int(input())
    # assert p % 4 == 3 and q % 4 == 3
    n = p * q
    seed = int(input())
    r = BBS(seed, l, n)
    # print("[+]random bytes sequence:", r)
    print(int(r, 2))
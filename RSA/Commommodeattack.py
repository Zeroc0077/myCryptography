# -*- encoding: utf-8 -*-
'''
@File    :   Commommodeattack.py
@Time    :   2023/04/17 10:25:29
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.utils import *


def CommomModeAttack(n, c1, c2, e1, e2):
    if e1 < e2:
        e1, e2 = e2, e1
        c1, c2 = c2, c1
    s = Exgcd(e1, e2)
    s1, s2 = s[0], s[1]
    if s[0] < 0:
        s1 = abs(s[0])
        c1 = inverse(c1, n)
    if s[1] < 0:
        s2 = abs(s[1])
        c2 = inverse(c2, n)
    m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
    return int(m)


if __name__ == "__main__":
    e1 = int(input())
    e2 = int(input())
    c1 = int(input())
    c2 = int(input())
    n = int(input())
    print(CommomModeAttack(n, c1, c2, e1, e2))

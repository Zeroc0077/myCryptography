# -*- encoding: utf-8 -*-
'''
@File    :   broadcast.py
@Time    :   2023/04/12 00:42:12
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.utils import *

def broadcast_attack(N, c):
    m = CRT(N, c)
    m = iroot(m, e)[0]
    return m

if __name__ == "__main__":
    n = int(input())
    e = int(input())
    c = []
    N = []
    for i in range(n):
        c.append(int(input()))
        N.append(int(input()))
    m = broadcast_attack(N, c)
    print(m)
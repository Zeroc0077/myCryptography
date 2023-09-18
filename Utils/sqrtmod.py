# -*- encoding: utf-8 -*-
'''
@File    :   sqrtmod.py
@Time    :   2023/04/27 17:56:41
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.Matrix import *
from Utils.number import *
from random import randint


def Lucas(p, x, y, k):
    mat = [[x, 1], [(p - y) % p, 0]]
    mat = Matpow(mat, k - 1, p)
    u = mat[0][0]
    v = (mat[0][0] * x + mat[1][0] * 2) % p
    return u, v


def sqrtmod(g, p) -> int:
    if p % 4 == 3:
        u = (p - 3) // 4
        y = pow(g, u + 1, p)
        if y * y % p != g:
            raise Exception('There is no solution.')
        return y
    elif p % 8 == 5:
        u = (p - 5) // 8
        z = pow(g, 2 * u + 1, p)
        if z % p == 1:
            return pow(g, u + 1, p)
        elif z % p == p - 1:
            return (2 * g * pow(4 * g, u, p)) % p
        else:
            raise Exception('There is no solution.')
    elif p % 8 == 1:
        u = (p - 1) // 8
        Y = g
        while True:
            X = randint(0, p)
            U, V = Lucas(p, X, Y, 4 * u + 1)
            if V * V % p == (4 * Y) % p:
                return (V * inverse(2, p)) % p
            elif U % p != 1 and U % p != p - 1:
                raise Exception('There is no solution.')

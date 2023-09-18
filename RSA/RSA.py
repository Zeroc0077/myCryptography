# -*- encoding: utf-8 -*-
'''
@File    :   RSA.py
@Time    :   2023/04/13 17:54:30
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
sys.dont_write_bytecode = True
from Utils.number import *


class RSA:
    @staticmethod
    def encrypt(m, e, n):
        return qpow(m, e, n)

    @staticmethod
    def decrypt(c, d, n):
        return qpow(c, d, n)

    @staticmethod
    def Qdecrypt(c, p, q, d):
        dp = inverse(d, p-1)
        dq = inverse(d, q-1)
        q1 = inverse(q, p)
        m1 = qpow(c, dp, p)
        m2 = qpow(c, dq, q)
        h = (q1*(m1-m2)) % p
        m = m2 + h*q
        return m


if __name__ == "__main__":
    p = int(input())
    q = int(input())
    e = int(input())
    m = int(input())
    mode = int(input())
    if mode == 1:
        res = RSA.encrypt(m, e, p*q)
        print(res)
    else:
        res = RSA.Qdecrypt(m, p, q, e)
        print(res)

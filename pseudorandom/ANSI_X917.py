# -*- encoding: utf-8 -*-
'''
@File    :   ANSI_X917.py
@Time    :   2023/04/11 23:33:12
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
sys.dont_write_bytecode = True
from Sysmetric_Cryptography.Block_Cipher import *

class ANSI_X917:
    def __init__(self, key1: int, key2: int) -> None:
        self.TD = TripDES(key1, key2)

    def Gen(self, date: int, iv: int) -> int:
        tmp = self.TD.encrypt(date)
        R = self.TD.encrypt(iv ^ tmp)
        V = self.TD.encrypt(R ^ tmp)
        return R, V


if __name__ == "__main__":
    iv = int(input().strip()[2:], 16)
    key1 = int(input().strip()[2:], 16)
    key2 = int(input().strip()[2:], 16)
    count = int(input())
    R, V = [], []
    ansi = ANSI_X917(key1, key2)
    for i in range(count):
        date = int(input().strip()[2:], 16)
        if i == 0:
            R.append(ansi.Gen(date, iv)[0])
            V.append(ansi.Gen(date, iv)[1])
        else:
            R.append(ansi.Gen(date, V[i-1])[0])
            V.append(ansi.Gen(date, V[i-1])[1])
    for i in R:
        print("0x" + hex(i)[2:].rjust(16, "0"))

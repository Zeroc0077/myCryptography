# -*- encoding: utf-8 -*-
'''
@File    :   Sbox.py
@Time    :   2023/03/22 11:21:19
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.utils import *


def Init_Sbox(SBox):
    """
    Initialize the SBox
    """
    for i in range(16):
        tmp = []
        for j in range(16):
            tmp.append(i*16 + j)
        SBox.append(tmp)


def Mapping_inverse(SBox):
    """
    Mapping the element to its inverse element
    """
    for i in SBox:
        for j in range(16):
            """
            The correlation is reduced by inverse element in finite field
            """
            i[j] = poly.inverse(poly(i[j])).value


def BytesTransformation(SBox):
    """
    apply bytes transformation
    """
    for i in SBox:
        for j in range(16):
            res = 0
            for k in range(8):
                """
                Spread by byte transformation
                """
                res += (((i[j] >> k) & 0x1) ^ ((i[j] >> ((k+4) % 8)) & 0x1) ^ ((i[j] >> ((k+5) % 8)) & 0x1) ^ (
                    (i[j] >> ((k+6) % 8)) & 0x1) ^ ((i[j] >> ((k+7) % 8)) & 0x1) ^ ((0x63 >> k) & 0x1)) << k
            i[j] = res


def invBytesTransformation(SBox):
    """
    apply inverse bytes transformation
    """
    for i in SBox:
        for j in range(16):
            res = 0
            for k in range(8):
                res += (((i[j] >> ((k+2) % 8)) & 0x1) ^ ((i[j] >> ((k+5) % 8)) & 0x1)
                        ^ ((i[j] >> ((k+7) % 8)) & 0x1) ^ ((0x05 >> k) & 0x1)) << k
            i[j] = res


def generate_inv():
    """
    generate the inverse SBox
    """
    inv_SBox = []
    Init_Sbox(inv_SBox)
    invBytesTransformation(inv_SBox)
    Mapping_inverse(inv_SBox)
    return inv_SBox


if __name__ == "__main__":
    SBox = []
    print("-----------------------------------Init--------------------------------------")
    Init_Sbox(SBox)
    for i in SBox:
        for j in i:
            print("0x" + hex(j)[2:].rjust(2, "0"), end=" ")
        print()
    print("-----------------------------------END---------------------------------------")
    print("-----------------------------------Map---------------------------------------")
    Mapping_inverse(SBox)
    for i in SBox:
        for j in i:
            print("0x" + hex(j)[2:].rjust(2, "0"), end=" ")
        print()
    print("-----------------------------------END---------------------------------------")
    print("----------------------------------Trans--------------------------------------")
    BytesTransformation(SBox)
    for i in SBox:
        for j in i:
            print("0x" + hex(j)[2:].rjust(2, "0"), end=" ")
        print()
    print("-----------------------------------END--------------------------------------")
    print("-----------------------------------Inv--------------------------------------")
    inv_SBox = generate_inv()
    for i in inv_SBox:
        for j in range(16):
            print("0x" + hex(i[j])[2:].rjust(2, "0"), end=" ")
        print()
    print("-----------------------------------END-------------------------------------")

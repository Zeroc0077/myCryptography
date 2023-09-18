# -*- encoding: utf-8 -*-
'''
@File    :   Hill_Known_pt_attack.py
@Time    :   2023/03/08 12:00:24
@Author  :   zeroc 
'''
import sys
sys.path.append(".")

from Utils.Matrix import *
from Utils.Exgcd import *
def generate_matrix(text: str, d: int) -> list:
    """
    generate a invertible matrix, the dimension of it is d
    """
    while True:
        res = []
        for i in range(d):
            res.append(text[i*d:(i+1)*d])
        if Exgcd(det(res), 26)[2] != 1:
            text = text[d:]
        else:
            return res

def attack(pt: str, ct: str, d: int) -> list:
    """
    compute the key:
    key = pt^-1 · ct
    """
    pt = [ord(i) - ord('a') for i in pt]
    ct = [ord(i) - ord('a') for i in ct]
    pt = generate_matrix(pt, d)
    ct = generate_matrix(ct, d)
    return multMatrix_mod(inv_mod(pt), ct)

if __name__ == "__main__":
    d = int(input())
    pt = input().strip()
    ct = input().strip()
    key = attack(pt, ct, d)
    for i in range(d):
        for j in range(d):
            if j != d-1:
                print(key[i][j], end=" ")
            else:
                print(key[i][j], end="")
        print()
    
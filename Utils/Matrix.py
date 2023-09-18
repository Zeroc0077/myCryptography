# -*- encoding: utf-8 -*-
'''
@File    :   Matrix.py
@Time    :   2023/03/02 18:14:37
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.utils import *

def multMatrix(a: list, b: list) -> list:
    """
    implement matrix multiplication
    """
    if len(b) != len(a[0]):
        raise Exception("[Error]Invalid rows")
    res = []
    row = len(a)
    column = len(b[0])
    for i in range(row):
        tmp = []
        for j in range(column):
            r = 0
            for k in range(len(b)):
                r += a[i][k] * b[k][j]
            tmp.append(r)
        res.append(tmp)
    return res


def Matmul(a, b, p):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] = (res[i][j] + a[i][k] * b[k][j]) % p
    return res


def Matpow(a, n, p):
    res = a
    tmp = a
    n -= 1
    while n:
        if n & 1:
            res = Matmul(res, tmp, p)
        tmp = Matmul(tmp, tmp, p)
        n >>= 1
    return res


def multMatrix_mod(a: list, b: list) -> list:
    """
    implement matrix multiplication
    """
    if len(b) != len(a[0]):
        raise Exception("[Error]Invalid rows")
    res = []
    row = len(a)
    column = len(b[0])
    for i in range(row):
        tmp = []
        for j in range(column):
            r = 0
            for k in range(len(b)):
                r += a[i][k] * b[k][j] % 26
            tmp.append(r % 26)
        res.append(tmp)
    return res


def submatrix(a: list, i: int, j: int) -> list:
    """
    find the submatrix of matrix

    Arguments:
    i -> the row that was deleted
    j -> the column that was deleted
    """
    row = len(a)
    column = len(a[0])
    C = [[a[x][y] for y in range(row) if y != j]
         for x in range(column) if x != i]
    return C


def det(a: list) -> int:
    """
    calc the det of the matrix
    """
    row = len(a)
    column = len(a[0])
    if row != column:
        raise Exception("[Error]It has to be a square matrix!")
    if (row == 1 and column == 1):  # ! the dimension of matrix is 1
        return a[0][0]
    elif (row == 2 and column == 2):  # ! the dimension of matrix is 2
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    else:
        value = 0
        for j in range(column):
            value += (((-1) ** (j + 2)) * a[0]
                      [j] * det(submatrix(a, 0, j)) % 26)
        return value % 26


def transpose(a: list) -> list:
    """
    compute the transpose of the matrix
    """
    row = len(a)
    column = len(a[0])
    res = []
    for i in range(column):
        tmp = []
        for j in range(row):
            tmp.append(a[j][i])
        res.append(tmp)
    return res


def inv_mod(a: list) -> list:
    """
    compute the modular inverse matrix
    """
    adj_matrix = []  # ! the adjoint matrix
    row = len(a)
    column = len(a[0])
    for i in range(row):
        tmp = []
        for j in range(column):
            tmp.append(((-1) ** (i + j + 2) * det(submatrix(a, i, j))) % 26)
        adj_matrix.append(tmp)
    inv = inverse(det(a), 26)
    for i in range(row):
        for j in range(column):
            adj_matrix[i][j] = (adj_matrix[i][j] * inv) % 26
    return transpose(adj_matrix)


if __name__ == "__main__":
    a = [[19, 13, 1], [9, 20, 20], [20, 17, 16]]
    for i in a:
        print(i)
    for i in inv_mod(a):
        print(i)

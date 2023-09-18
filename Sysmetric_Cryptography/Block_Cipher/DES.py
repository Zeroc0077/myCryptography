# -*- encoding: utf-8 -*-
'''
@File    :   DES.py
@Time    :   2023/03/08 09:28:52
@Author  :   zeroc
'''
S_box = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

p1 = [57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4]

p = [14, 17, 11, 24,  1,  5,  3, 28, 15,  6, 21, 10,
     23, 19, 12,  4, 26,  8, 16,  7, 27, 20, 13,  2,
     41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
     44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

IP = [58, 50, 42, 34, 26, 18, 10,  2, 60, 52, 44, 36, 28, 20, 12,  4,
      62, 54, 46, 38, 30, 22, 14,  6, 64, 56, 48, 40, 32, 24, 16,  8,
      57, 49, 41, 33, 25, 17,  9,  1, 59, 51, 43, 35, 27, 19, 11,  3,
      61, 53, 45, 37, 29, 21, 13,  5, 63, 55, 47, 39, 31, 23, 15,  7]

inv_IP = [40,  8, 48, 16, 56, 24, 64, 32, 39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30, 37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28, 35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26, 33,  1, 41,  9, 49, 17, 57, 25]

E = [32,  1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32,  1]

P_box = [16,  7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26,  5, 18, 31, 10,
         2,  8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25]


class DES():
    def __init__(self, key: int) -> None:
        """
        Initalize a DES cipher

        key -> the 64-bit key
        """
        self.key = bin(key)[2:].rjust(64, "0")
        self.subkeys = []

#!------------------------------Generate round key--------------------------------------
    def select_permutation_1(self):
        """
        The first round of selective permutation
        select 56-bit subkey from 64-bit key, and divide it into two parts
        """
        if len(self.key) != 64:
            raise Exception("[Error]The length of key must be 64 bit")
        #! transform to int
        return [int(self.key[i-1]) for i in p1[:28]], [int(self.key[i-1]) for i in p1[28:]]

    def select_permutation_2(self, subkey: list) -> list:
        """
        The second round of selective permutation
        select 48-bit subkey from 56-bit key
        """
        if len(subkey) != 56:
            raise Exception("[Error]The length of subkey must be 56")
        return [subkey[i-1] for i in p]

    def leftRotation(self, a: list, off: int) -> list:
        """
        Implement loop left shift
        """
        return a[off:] + a[:off]

    def keyGen(self):
        """
        Generate 16 round key

        Logical flow:
        64-bit key -> select_permutaion_1 -> 56-bit key(left + right)
        leftRotation(left) + leftRotation(right) -> round key 0
        leftRotation(left) + leftRotation(right) -> round key 1
        leftRotation(left) + leftRotation(right) -> round key 2
        ...
        """
        if len(self.key) != 64:
            raise Exception("[Error]The length of initial key must be 64")
        left, right = self.select_permutation_1()
        # ! The leftrotation offset array
        off = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

        for i in range(16):
            left = self.leftRotation(left, off[i])
            right = self.leftRotation(right, off[i])
            self.subkeys.append(self.select_permutation_2(left+right))
#!---------------------------------encryption--------------------------------------

    def Initial_permutation(self, text: list) -> list:
        """
        The initial permutation
        """
        return [int(text[i-1]) for i in IP]  # ! transform to int

    def inv_Initial_permutation(self, text: list) -> list:
        """
        The inverse initial permutation
        """
        return [text[i-1] for i in inv_IP]

    def Expand(self, text: list) -> list:
        """
        Expand permutation

        32-bit text -> 48-bit text
        """
        if len(text) != 32:
            raise Exception("[Error]The length must be 32")
        return [text[i-1] for i in E]

    def P_permutation(self, text: list) -> list:
        """
        The P permutation
        """
        if len(text) != 32:
            raise Exception("[Error]The length must be 32")
        return [text[i-1] for i in P_box]

    def S_transformation(self, text: list) -> list:
        """
        S_box transformation
        48-bit text -> 32-bit text
        """
        if len(text) != 48:
            raise Exception("[Error]The length must be 48")

        res = []
        # ! the first bit and the last bit determine the subarray and the left determine the index
        for i in range(0, len(text), 6):
            tmp = int(str(text[i])+str(text[i+5])+str(text[i+1]) +
                      str(text[i+2])+str(text[i+3])+str(text[i+4]), 2)
            m = bin(S_box[i // 6][tmp])[2:].rjust(4, "0")
            for j in m:
                res.append(int(j))
        return res

    def Feistel(self, text: list, subkey: list) -> list:
        """
        Implement Feistel encrypt
        Expand(text) xor subkey -> S_transform -> p_permutation
        """
        if len(text) != 32 or len(subkey) != 48:
            raise Exception("[Error]The length Error")
        text = self.Expand(text)
        tmp = [i ^ j for i, j in zip(text, subkey)]
        tmp = self.S_transformation(tmp)
        tmp = self.P_permutation(tmp)

        return tmp

    def Round(self, left: list, right: list, subkey: list):
        """
        Round encryption:
        L' = R
        R' = L ^ Feistel(R, subkey)
        """
        tmp = self.Feistel(right, subkey)
        tmp = [i ^ j for i, j in zip(left, tmp)]

        return right, tmp

    def encrypt(self, plaintext: int) -> int:
        plaintext = bin(plaintext)[2:].rjust(64, "0")  # ! make up 64 bits

        m = self.Initial_permutation(plaintext)  # ! IP permutration
        left, right = m[:32], m[32:]
        for i in range(16):
            left, right = self.Round(left, right, self.subkeys[i])
        tmp = self.inv_Initial_permutation(
            right + left)  # ! inverse IP permutation
        return int("".join(str(i) for i in tmp), 2)

    def decrypt(self, ciphertext: int) -> int:
        ciphertext = bin(ciphertext)[2:].rjust(64, "0")  # ! make up 64 bits
        # ! invert the subkeys for decryption
        subkeys = self.subkeys[::-1]

        m = self.Initial_permutation(ciphertext)  # ! IP permutation
        left, right = m[:32], m[32:]
        for i in range(16):
            left, right = self.Round(left, right, subkeys[i])
        tmp = self.inv_Initial_permutation(
            right + left)  # ! inverse IP permutation
        return int("".join(str(i) for i in tmp), 2)


class TripDES():  # ! EDE2
    def __init__(self, key1: int, key2: int) -> None:
        """
        Initialize a TripDES with two encrypt keys
        """
        self.key1 = key1
        self.key2 = key2
        self.des1 = DES(key1)
        self.des2 = DES(key2)
        self.des1.keyGen()
        self.des2.keyGen()

    def encrypt(self, plaintext: int) -> int:
        """
        encrypt: C = E1(D2(E1(P)))
        """
        ciphertext = self.des1.encrypt(plaintext)
        ciphertext = self.des2.decrypt(ciphertext)
        ciphertext = self.des1.encrypt(ciphertext)
        return ciphertext

    def decrypt(self, ciphertext: int) -> int:
        """
        decrypt: P = D1(E2(D1(C)))
        """
        plaintext = self.des1.decrypt(ciphertext)
        plaintext = self.des2.encrypt(plaintext)
        plaintext = self.des1.decrypt(plaintext)
        return plaintext


if __name__ == "__main__":
    from Crypto.Util.number import *
    key = 0x12345678
    pt1 = 0x75DBA1CAC6A1FBFB
    pt2 = 0x7C1361AEEEE6E996
    pt3 = 0x3EC239DA85BE7D63
    D = DES(key)
    D.keyGen()
    ciphertext1 = D.decrypt(pt1)
    ciphertext2 = D.decrypt(pt2)
    ciphertext3 = D.decrypt(pt3)
    print(long_to_bytes(ciphertext1)[::-1] + long_to_bytes(ciphertext2)[::-1] + long_to_bytes(ciphertext3)[::-1])
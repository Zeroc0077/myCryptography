# -*- encoding: utf-8 -*-
'''
@File    :   Classic_Cipher.py
@Time    :   2023/02/27 09:58:22
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
from Utils.Matrix import *
from Utils.number import *


class Caesar():
    def __init__(self, k: int, m: int = 26, base: int = 97) -> None:
        """
        Initialize a caesar cipher

        Arguments:
        k -> displacement
        m -> the module, the default is 26
        base -> depends on uppercase or lowercase, the default is 97
        """
        self.k = k
        self.m = m
        self.base = base

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(p, k) = (p + k) mod m
        """
        ciphertext = ""
        for i in plaintext:
            if self.base <= ord(i) < self.base + 26:
                ciphertext += chr((ord(i) - self.base + self.k) %
                                  self.m + self.base)
            else:
                ciphertext += i
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: p = D(C, k) = (C - k) mod m
        """
        plaintext = ""
        for i in ciphertext:
            if self.base <= ord(i) < self.base + 26:
                plaintext += chr((ord(i) - self.base - self.k) %
                                 self.m + self.base)
            else:
                plaintext += i
        return plaintext


class Sample():
    def __init__(self, k: int, m: int = 26, base: int = 97) -> None:
        """
        Initialize a sampling cipher

        Arguments:
        k -> multiplier
        m -> the module, default is 26
        base -> depends on uppercase or lowercase, the default is 97
        """
        if Exgcd(k, m)[2] != 1:
            raise Exception("[Error]k and m must be mutual prime!")
        self.k = k
        self.m = m
        self.base = base
        self.d = inverse(k, m)

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(p, k) = (k * p) mod m
        """
        ciphertext = ""
        for i in plaintext:
            if self.base <= ord(i) < self.base + self.m:
                ciphertext += chr(((ord(i) - self.base) *
                                  self.k % self.m) + self.base)
            else:
                ciphertext += i
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: p = D(C, k) = (C * inv(k, m)) mod m
        """
        plaintext = ""
        for i in ciphertext:
            if self.base <= ord(i) < self.base + 26:
                plaintext += chr(((ord(i) - self.base) * self.d %
                                 self.m) + self.base)
            else:
                ciphertext += i
        return plaintext


class Affine():
    def __init__(self, k: int, b: int, m: int = 26, base: int = 97) -> None:
        """
        Initialize a affine cipher

        Arguments:
        k -> multiplier
        b -> displacement
        m -> module, default is 26
        base -> depends on uppercase or lowercase, the default is 97
        """
        if Exgcd(m, k)[2] != 1:
            raise Exception("[Error]k and m must be mutual prime")
        self.k = k
        self.b = b
        self.m = m
        self.base = base
        self.d = inverse(k, m)

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(P, k, b) = (k * P + b) % m
        """
        ciphertext = ""
        for i in plaintext:
            if self.base <= ord(i) < self.base + self.m:
                ciphertext += chr(((ord(i) - self.base) *
                                  self.k + self.b) % self.m + self.base)
            else:
                ciphertext += i
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: 
        d = inverse(k, m)
        P = D(C, k, b) = ((C - b) * d) % m
        """
        plaintext = ""
        for i in ciphertext:
            if self.base <= ord(i) < self.base + self.m:
                plaintext += chr((((ord(i) - self.base) - self.b)
                                 * self.d) % self.m + self.base)
            else:
                plaintext += i
        return plaintext


class SingleTable():
    def __init__(self, From: str, To: str, l: int = 26, base: int = 97) -> None:
        """
        Initailize the single table cipher

        Argumnets:
        From -> the original alphabet
        To -> the target alphabet
        l -> the length of table
        base -> depends on uppercase or lowercase, the default is 97
        """
        if len(From) != l or len(To) != l:
            raise Exception("[Error]Wrong table length")
        dic = {}
        for i, j in zip(From, To):
            dic[i] = j
        self.dic = dic
        self.list_value = list(self.dic.values())
        self.list_key = list(self.dic.keys())
        self.base = base

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(P) = table[P]
        """
        ciphertext = ""
        for i in plaintext:
            ciphertext += self.dic[i]
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: P = D(C) = table'[C]
        """
        plaintext = ""
        for i in ciphertext:
            plaintext += self.list_key[self.list_value.index(i)]
        return plaintext


class Vigenere():
    def __init__(self, key: str, base: int = 97) -> None:
        """
        Initialize Vigenere cipher

        Arguments:
        key -> the key of the cipher
        base -> depends on uppercase or lowercase, the default is 97
        """
        self.key = key
        self.l = len(key)
        self.base = base

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(P, k)
        """
        ciphertext = ""
        for i in range(len(plaintext)):
            ciphertext += chr((ord(plaintext[i]) + ord(self.key[i %
                              self.l]) - 2 * self.base) % 26 + self.base)
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: P = D(C, k)
        """
        plaintext = ""
        for i in range(len(ciphertext)):
            plaintext += chr((ord(ciphertext[i]) -
                             ord(self.key[i % self.l])) % 26 + self.base)
        return plaintext


class Furnham():
    def __init__(self, key: str) -> None:
        """
        Initialize Furnham cipher

        Arguments:
        key -> the key of the cipher
        """
        self.key = key
        self.l = len(key)

    def encrypt(self, plaintext: str) -> str:
        """
        xor means the encryption is the same as the decryption
        """
        ciphertext = ""
        for i in range(len(plaintext)):
            ciphertext += chr(ord(plaintext[i]) ^ ord(self.key[i % self.l]))
        return ciphertext


class Fence():
    def __init__(self, key: int) -> None:
        """
        Initialize the fence cipher

        Arguments:
        key -> the key of the cipher
        """
        self.key = key

    def slice(self, origin: str, l: int) -> list:
        """
        divide the string into slice
        """
        res = []
        for i in range(0, len(origin), l):
            res.append(origin[i:i+l].ljust(l, "*"))  # ! * stands for ""
        return res

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt
        """
        ciphertext = ""
        plaintext = self.slice(plaintext, self.key)  # ! divide into groups
        for i in range(self.key):
            for j in plaintext:
                if j[i] != "*":
                    ciphertext += j[i]  # ! concat ciphertext
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt
        """
        plaintext = ""
        #! if len(ciphertext) = 0 mod key, just divide it into len(ciphertext) // key groups
        if len(ciphertext) % self.key == 0:
            l = len(ciphertext) // self.key
            ciphertext = self.slice(ciphertext, l)
            for i in range(l):
                for j in ciphertext:
                    plaintext += j[i]
            return plaintext
        l = (len(ciphertext) // self.key)
        dis = len(ciphertext) - l * self.key
        suffix = ""
        for i in range(1, dis+1):
            suffix += ciphertext[i * l]
            ciphertext = ciphertext[:i*l] + ciphertext[i*l+1:]
        ciphertext = self.slice(ciphertext, l)
        for i in range(l):
            for j in ciphertext:
                plaintext += j[i]
        return plaintext + suffix


class Hill():
    def __init__(self, key: list) -> None:
        """
        Initialize a Hill cipher

        Arguments:
        key -> the matrix
        l -> the dimension of matrix
        """
        self.key = key
        self.l = len(key)

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt: C = E(p, k) = p * matrix(k)
        """
        ciphertext = ""
        for i in range(0, len(plaintext), self.l):
            tmp = [[ord(j)-ord('a') for j in plaintext[i:i+self.l]]]
            res = multMatrix_mod(tmp, self.key)
            ciphertext += "".join(chr(k+ord('a')) for k in res[0])
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        decrypt: p = D(C, k) = C * inv_key(k) 
        """
        plaintext = ""
        inv_key = inv_mod(self.key)
        for i in range(0, len(ciphertext), self.l):
            tmp = [[ord(j)-ord('a') for j in ciphertext[i:i+self.l]]]
            res = multMatrix_mod(tmp, inv_key)
            plaintext += "".join(chr(k+ord('a')) for k in res[0])
        return plaintext


class MatrixCipher():
    def __init__(self, key: str) -> None:
        """
        Initialize a Matrix Cipher

        Arguments:
        key -> the key of the cipher
        """
        self.key = key
        self.l = len(key)

    def str2matrix_key(self, s):
        """
        transform the str to matrix
        """
        if len(s) % self.l != 0:
            raise Exception("[Error]The length of str error")
        s = list(s)
        M = []
        for i in range(0, len(s), self.l):
            m = []
            for j in range(i, i+self.l):
                m.append(s[j])
            M.append(m)
        return M

    def str2matrix_key_rev(self, s):
        """
        transform the str to matrix
        """
        s = list(s)
        M = []
        for i in range(0, len(s), len(s) // self.l):
            m = []
            for j in range(i, i+(len(s) // self.l)):
                m.append(s[j])
            M.append(m)
        return M

    def encrypt(self, plaintext: str) -> str:
        """
        encrypt
        choose the column with key sequence
        """
        ciphertext = ""
        plaintext = self.str2matrix_key(plaintext)
        for i in range(1, self.l+1):
            for j in plaintext:
                ciphertext += j[self.key.index(str(i))]
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        n = len(ciphertext) // self.l
        ciphertext = self.str2matrix_key_rev(ciphertext)
        for i in range(n):
            for j in self.key:
                plaintext += ciphertext[int(j)-1][i]
        return plaintext


if __name__ == "__main__":
    print("[Caesar]--------Test fot caesar cipher--------")
    caesar = Caesar(3)
    plaintext = "hello every body"
    ciphertext = caesar.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = caesar.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Caesar]----------------End-------------------")
    print("[Sample]--------Test fot sampling cipher--------")
    sample = Sample(3)
    plaintext = "mycryptography"
    ciphertext = sample.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = sample.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Sample]------------------End-------------------")
    print("[Affine]--------Test fot Affine cipher--------")
    affine = Affine(3, 17)
    plaintext = "thisisatestforaffinecipher"
    ciphertext = affine.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = affine.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Affine]-----------------End------------------")
    print("[SingleTable]--------Test fot Singletable cipher--------")
    From = "abcdefghijklmnopqrstuvwxyz"
    To = "qazwsxedcrfvtgbyhnujmiklop"
    st = SingleTable(From, To)
    plaintext = "doyouwannatodance"
    ciphertext = st.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = st.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[SingleTable]--------------------End---------------------")
    print("[Vigenere]--------Test fot Vigenere cipher--------")
    k = "interesting"
    v = Vigenere(k)
    plaintext = "zhonghuaminzuweidafuxing"
    ciphertext = v.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = v.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Vigenere]------------------End-------------------")
    print("[Furnham]--------Test fot Furnham cipher--------")
    k = "!@#$%^&"
    f = Furnham(k)
    plaintext = "kfccrazythursday"
    ciphertext = f.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = f.encrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Furnham]------------------End-------------------")
    print("[Fence]--------Test fot Fence cipher--------")
    k = 3
    f = Fence(k)
    plaintext = "whateverisworthdoingisworthdoingwellab"
    ciphertext = f.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = f.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Fence]----------------End------------------")
    print("[Matrix]--------Test fot Matrix cipher--------")
    k = "4312567"
    mc = MatrixCipher(k)
    plaintext = "attackpostponeduntiltwoamxyz"
    ciphertext = mc.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = mc.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Matrix]----------------End------------------")
    print("[Hill]--------Test fot Hill cipher--------")
    k = [[9, 4], [5, 7]]
    H = Hill(k)
    plaintext = "meetmeatbuaa"
    ciphertext = H.encrypt(plaintext)
    print("[ciphertext]", ciphertext)
    plaintext = H.decrypt(ciphertext)
    print("[plaintext]", plaintext)
    print("[Matrix]--------------End-----------------")

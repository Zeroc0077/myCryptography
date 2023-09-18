# -*- encoding: utf-8 -*-
'''
@File    :   SM3.py
@Time    :   2023/05/09 15:35:27
@Author  :   zeroc 
'''
from math import ceil


class SM3:
    def __init__(self) -> None:
        """
        Implement SM3 hash algorithm
        """
        self.IV = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
        self.T = [0x79cc4519] * 16 + [0x7a879d8a] * 48

    def _padding(self, msg: bytes) -> int:
        """
        padding the message to n*512 bits
        """
        value = int.from_bytes(msg, "big")
        length = len(msg) * 8
        k = 448 - (length + 1) % 512
        if k < 0:
            k += 512
        value = (value << 1 | 1) << (k + 64) | length
        return value

    def _Rotation(self, x: int, n: int) -> int:
        """
        cyclic left shift
        """
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def _FF(self, X, Y, Z, j):
        """
        FF function
        """
        if j < 16:
            return X ^ Y ^ Z
        else:
            return (X & Y) | (X & Z) | (Y & Z)

    def _GG(self, X, Y, Z, j):
        """
        GG function
        """
        if j < 16:
            return X ^ Y ^ Z
        else:
            return (X & Y) | ((~X) & Z)

    def _P0(self, X):
        """
        P0 function
        """
        return X ^ self._Rotation(X, 9) ^ self._Rotation(X, 17)

    def _P1(self, X):
        """
        P1 function
        """
        return X ^ self._Rotation(X, 15) ^ self._Rotation(X, 23)

    def _CF(self, V, B):
        """
        compression function
        """
        # message expansion
        W = []
        for i in range(68):
            if i < 16:
                W.append(B >> (512 - 32 * (i + 1)) & 0xFFFFFFFF)
            else:
                W.append(self._P1(W[i - 16] ^ W[i - 9] ^ self._Rotation(
                    W[i - 3], 15)) ^ self._Rotation(W[i - 13], 7) ^ W[i - 6])
        W_ = []
        for i in range(64):
            W_.append(W[i] ^ W[i + 4])
        M = []
        for i in range(8):
            M.append((V >> (256 - 32 * (i + 1))) & 0xFFFFFFFF)
        # compression
        for i in range(64):
            SS1 = self._Rotation((self._Rotation(
                M[0], 12) + M[4] + self._Rotation(self.T[i], i % 32)) & 0xFFFFFFFF, 7)
            SS2 = SS1 ^ self._Rotation(M[0], 12)
            TT1 = (self._FF(M[0], M[1], M[2], i) +
                   M[3] + SS2 + W_[i]) & 0xFFFFFFFF
            TT2 = (self._GG(M[4], M[5], M[6], i) +
                   M[7] + SS1 + W[i]) & 0xFFFFFFFF
            M[3] = M[2]
            M[2] = self._Rotation(M[1], 9)
            M[1] = M[0]
            M[0] = TT1
            M[7] = M[6]
            M[6] = self._Rotation(M[5], 19)
            M[5] = M[4]
            M[4] = self._P0(TT2)
        # update V
        res = 0
        for i in range(8):
            res = (res << 32) | M[i]
        return V ^ res

    def hash(self, msg) -> bytes:
        if type(msg) == str:
            msg = msg.encode("utf-8")
        value = self._padding(msg)
        iv = self.IV
        block_count = ceil(value.bit_length() / 512)
        for i in range(block_count):
            block = value >> (512 * (block_count - i - 1))
            iv = self._CF(iv, block)
        return iv.to_bytes(32, "big")


if __name__ == "__main__":
    msg = input().strip("\n")
    sm3 = SM3()
    print(sm3.hash(msg).hex())

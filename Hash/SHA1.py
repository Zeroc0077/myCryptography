# -*- encoding: utf-8 -*-
'''
@File    :   SHA1.py
@Time    :   2023/05/04 17:17:25
@Author  :   zeroc 
'''
from math import ceil


class SHA1:
    def __init__(self) -> None:
        """
        Implementation of SHA-1
            -self.H: initial hash value
            -self.KT: constant table
        """
        self.H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
        self.KT = [0x5A827999] * 20 + [0x6ED9EBA1] * \
            20 + [0x8F1BBCDC] * 20 + [0xCA62C1D6] * 20

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

    def _F(self, t: int, B: int, C: int, D: int) -> int:
        """
        F function
        """
        if t < 20:
            return (B & C) | ((~B) & D)
        elif t < 40:
            return B ^ C ^ D
        elif t < 60:
            return (B & C) | (B & D) | (C & D)
        else:
            return B ^ C ^ D

    def _process(self, value: int, H) -> None:
        """
        process a 512 bits block
        """
        W = [0] * 80
        for t in range(16):
            W[t] = value >> (512 - 32 * (t + 1)) & 0xFFFFFFFF
        for t in range(16, 80):
            W[t] = self._Rotation(W[t - 3] ^ W[t - 8] ^
                                  W[t - 14] ^ W[t - 16], 1)
        A, B, C, D, E = H
        for t in range(80):
            TEMP = (self._Rotation(A, 5) + self._F(t, B, C, D) +
                    E + W[t] + self.KT[t]) & 0xFFFFFFFF
            E = D
            D = C
            C = self._Rotation(B, 30)
            B = A
            A = TEMP
        return [(i + j) & 0xFFFFFFFF for i, j in zip(H, [A, B, C, D, E])]

    def hash(self, msg) -> bytes:
        """
        hash the message
        """
        if type(msg) == str:
            msg = msg.encode("utf-8")
        value = self._padding(msg)
        block_count = ceil(value.bit_length() / 512)
        H = self.H
        for i in range(block_count):
            H = self._process(value >> (512 * (block_count - i - 1)), H)
        return b"".join([i.to_bytes(4, "big") for i in H])

    def HMAC(self, msg: str, key) -> bytes:
        """
        calculate HMAC
        """
        if type(key) == str:
            key = key.encode("utf-8")
        l = ceil(len(key) / 64) * 64 - len(key)
        key += b"\x00" * l
        o_key_pad = bytes([i ^ 0x5C for i in key])
        i_key_pad = bytes([i ^ 0x36 for i in key])
        return self.hash(o_key_pad + self.hash(i_key_pad + msg.encode('utf-8')))


if __name__ == "__main__":
    # key = bytes.fromhex(input().strip())
    # msg = input().strip()
    # print(SHA1().HMAC(msg, key).hex())
    msg = input().strip("\n").encode("utf-8")
    sha1 = SHA1()
    print(sha1.hash(msg).hex())

# -*- encoding: utf-8 -*-
'''
@File    :   SM2.py
@Time    :   2023/05/01 15:55:51
@Author  :   zeroc 
'''
import sys
import os
sys.dont_write_bytecode = True
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from Hash.SM3 import *
from hashlib import sha256
from EllipticCurve import *
from math import log2


class SM2:
    def __init__(self, p: int, E: EllipticCurve, G: EllipticCurve_point, n: int = 0) -> None:
        """
        implementation of SM2 algorithm with the sha256 hash function
        Args:
            p: the prime of the curve
            E: the elliptic curve
            G: the base point
            n: the order of the base point
        """
        self.p = p
        self.E = E
        self.G = G
        self.n = n
        self.hash = SM3()

    def _KDF(self, Z: bytes, klen: int) -> bytes:
        """
        Key Derivation Function
        Args:
            Z: the input string
            klen: the bitlength of the output
        """
        ct = 1
        v = b''
        while len(v) < klen:
            v += sha256(Z + ct.to_bytes(4, 'big')).digest()
            ct += 1
        return v[:klen]

    def encrypt(self, plaintext: bytes, public_key: EllipticCurve_point, k: int, Par: int) -> bytes:
        """
        Encrypt the plaintext with the public key
        Args:
            plaintext: the plaintext to be encrypted
            public_key: the public key of the receiver
            k: the random number
            Par: the bitlength of the point
        """
        klen = len(plaintext)  # the bytelength of the plaintext
        C1 = self.G * k
        x1 = C1.x.to_bytes(Par // 8, 'big')
        y1 = C1.y.to_bytes(Par // 8, 'big')
        Q = public_key * k
        x2 = Q.x.to_bytes(Par // 8, 'big')
        y2 = Q.y.to_bytes(Par // 8, 'big')
        t = self._KDF(x2+y2, klen)
        C2 = bytes([t[i] ^ plaintext[i] for i in range(len(plaintext))])
        C3 = sha256(x2 + plaintext + y2).digest()
        # return C1 + C3 + C2
        # PC = 0x04
        return int(4).to_bytes(1, 'big') + x1 + y1 + C2 + C3

    def decrypt(self, ciphertext: bytes, private_key: int, Par: int) -> bytes:
        """
        Decrypt the ciphertext with the private key
        Args:
            ciphertext: the ciphertext to be decrypted
            private_key: the private key of the receiver
            Par: the bitlength of the point
        """
        klen = len(ciphertext[Par//4+1:-32])
        C1 = self.E(int.from_bytes(
            ciphertext[1:Par//8+1], 'big'), int.from_bytes(ciphertext[Par//8+1:Par//4+1], 'big'))
        Q = C1 * private_key
        x2 = Q.x.to_bytes(Par // 8, 'big')
        y2 = Q.y.to_bytes(Par // 8, 'big')
        t = self._KDF(x2+y2, klen)
        plaintext = bytes([t[i] ^ ciphertext[Par//4+1+i]
                          for i in range(len(t))])
        C3 = sha256(x2 + plaintext + y2).digest()
        # test if the ciphertext is valid
        if C3 == ciphertext[-32:]:
            return plaintext
        else:
            return b''

    def keyexchange_sender(self, private_key: int, public_key: EllipticCurve_point, h: int, r: int, Par: int, IDa: bytes, IDb: bytes, klen: int, RB: EllipticCurve_point = None, SB: bytes = None):
        """
        Implementation of SM2 key exchange for sender
        Args:
            private_key: the private key of the sender
            public_key: the public key of the receiver
            RB: the received point
            h: the cofactor of the curve
            r: the random number
            Par: the bitlength of the point
            IDa, IDb: the ID of the sender and the receiver
            klen: the bitlength of the key
            SB: the signature of the receiver
        """
        PA = self.G * private_key
        ENTLA = (len(IDa) * 8).to_bytes(2, 'big')
        ENTLB = (len(IDb) * 8).to_bytes(2, 'big')
        Za = sha256(ENTLA + IDa + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par //
                    8, 'big') + self.G.y.to_bytes(Par // 8, 'big') + PA.x.to_bytes(Par // 8, 'big') + PA.y.to_bytes(Par // 8, 'big')).digest()
        Zb = sha256(ENTLB + IDb + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par // 8, 'big') +
                    self.G.y.to_bytes(Par // 8, 'big') + public_key.x.to_bytes(Par // 8, 'big') + public_key.y.to_bytes(Par // 8, 'big')).digest()
        RA = self.G * r
        yield RA
        w = ceil(ceil(log2(self.n)) / 2) - 1
        x1 = 2 ** w + (RA.x & (2 ** w - 1))
        tA = (private_key + x1 * r) % self.n
        tmp = (RB.x, RB.y)
        if not self.E.Curve_test(tmp):
            raise Exception(
                "[Error]Key Exchange Failed for RB is not on the curve")
        x2 = 2 ** w + (RB.x & (2 ** w - 1))
        U = (public_key + RB * x2) * (h * tA)
        if U == self.E.infinity:
            raise Exception("[Error]Key Exchange Failed for U is infinity")
        K = self._KDF(U.x.to_bytes(Par // 8, 'big') +
                      U.y.to_bytes(Par // 8, 'big') + Za + Zb, klen // 8)
        S = sha256(int(2).to_bytes(1, 'big') + U.y.to_bytes(Par // 8, 'big') + sha256(U.x.to_bytes(Par // 8, 'big') + Za + Zb + RA.x.to_bytes(
            Par // 8, 'big') + RA.y.to_bytes(Par // 8, 'big') + RB.x.to_bytes(Par // 8, 'big') + RB.y.to_bytes(Par // 8, 'big')).digest()).digest()
        if S != SB:
            raise Exception(
                "[Error]Key Exchange Failed for S is not equal to SB")
        SA = sha256(int(3).to_bytes(1, 'big') + U.y.to_bytes(Par // 8, 'big') + sha256(U.x.to_bytes(Par // 8, 'big') + Za + Zb + RA.x.to_bytes(
            Par // 8, 'big') + RA.y.to_bytes(Par // 8, 'big') + RB.x.to_bytes(Par // 8, 'big') + RB.y.to_bytes(Par // 8, 'big')).digest()).digest()
        yield SA

    def keyexchange_receiver(self, private_key: int, public_key: EllipticCurve_point, RA: EllipticCurve_point, h: int, r: int, Par: int, IDa: bytes, IDb: bytes, klen: int, SA: bytes = None):
        """
        Implementation of SM2 key exchange for receiver
        Args:
            private_key: the private key of the receiver
            public_key: the public key of the sender
            RA: the received point
            h: the cofactor of the curve
            r: the random number
            Par: the bitlength of the point
            IDa, IDb: the ID of the sender and the receiver
            klen: the bitlength of the key
            SA: the signature of the sender
        """
        PB = self.G * private_key
        ENTLA = (len(IDa) * 8).to_bytes(2, 'big')
        ENTLB = (len(IDb) * 8).to_bytes(2, 'big')
        Za = sha256(ENTLA + IDa + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par // 8, 'big') +
                    self.G.y.to_bytes(Par // 8, 'big') + public_key.x.to_bytes(Par // 8, 'big') + public_key.y.to_bytes(Par // 8, 'big')).digest()
        Zb = sha256(ENTLB + IDb + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par //
                    8, 'big') + self.G.y.to_bytes(Par // 8, 'big') + PB.x.to_bytes(Par // 8, 'big') + PB.y.to_bytes(Par // 8, 'big')).digest()
        RB = self.G * r
        w = ceil(ceil(log2(self.n)) / 2) - 1
        x2 = 2 ** w + (RB.x & (2 ** w - 1))
        tB = (private_key + x2 * r) % self.n
        tmp = (RA.x, RA.y)
        if not self.E.Curve_test(tmp):
            raise Exception(
                "[Error]Key Exchange Failed for RA is not on the curve")
        x1 = 2 ** w + (RA.x & (2 ** w - 1))
        V = (public_key + RA * x1) * (h * tB)
        if V == self.E.infinity:
            raise Exception("[Error]Key Exchange Failed for V is infinity")
        K = self._KDF(V.x.to_bytes(Par // 8, 'big') +
                      V.y.to_bytes(Par // 8, 'big') + Za + Zb, klen // 8)
        SB = sha256(int(2).to_bytes(1, 'big') + V.y.to_bytes(Par // 8, 'big') + sha256(V.x.to_bytes(Par // 8, 'big') + Za + Zb + RA.x.to_bytes(
            Par // 8, 'big') + RA.y.to_bytes(Par // 8, 'big') + RB.x.to_bytes(Par // 8, 'big') + RB.y.to_bytes(Par // 8, 'big')).digest()).digest()
        yield RB, SB
        S = sha256(int(3).to_bytes(1, 'big') + V.y.to_bytes(Par // 8, 'big') + sha256(V.x.to_bytes(Par // 8, 'big') + Za + Zb + RA.x.to_bytes(
            Par // 8, 'big') + RA.y.to_bytes(Par // 8, 'big') + RB.x.to_bytes(Par // 8, 'big') + RB.y.to_bytes(Par // 8, 'big')).digest()).digest()
        if S != SA:
            raise Exception(
                "[Error]Key Exchange Failed for S is not equal to SA")
        print("[Success]Key Exchange Success")
        print("[Success]The shared key is", K.hex())
        yield True

    def Sign(self, private_key: int, message: bytes, Par: int, IDa: bytes, k: int):
        """
        Implementation of SM2 signature
        Args:
            private_key: the private key of the signer
            message: the message to be signed
            Par: the bitlength of the point
            IDa: the ID of the signer
            k: the random number
        """
        PA = self.G * private_key
        ENTLA = (len(IDa) * 8).to_bytes(2, 'big')
        Za = self.hash.hash(ENTLA + IDa + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par //
                                                                                                                                      8, 'big') + self.G.y.to_bytes(Par // 8, 'big') + PA.x.to_bytes(Par // 8, 'big') + PA.y.to_bytes(Par // 8, 'big'))
        e = int(self.hash.hash(Za + message).hex(), 16)
        K = self.G * k
        r = (e + K.x) % self.n
        if r == 0 or r + k == self.n:
            pass
        s = (pow(1 + private_key, -1, self.n) * (k - r * private_key)) % self.n
        if s == 0:
            pass
        return r, s

    def Verify(self, public_key: EllipticCurve_point, message: bytes, Par: int, IDa: bytes, r: int, s: int):
        """
        Implementation of SM2 signature verification
        Args:
            public_key: the public key of the signer
            message: the message to be signed
            Par: the bitlength of the point
            IDa: the ID of the signer
            r: the first part of the signature
            s: the second part of the signature
        """
        if r < 1 or r > self.n or s < 1 or s > self.n:
            return False
        ENTLA = (len(IDa) * 8).to_bytes(2, 'big')
        Za = self.hash.hash(ENTLA + IDa + self.E.a.to_bytes(Par // 8, 'big') + self.E.b.to_bytes(Par // 8, 'big') + self.G.x.to_bytes(Par //
                                                                                                                                      8, 'big') + self.G.y.to_bytes(Par // 8, 'big') + public_key.x.to_bytes(Par // 8, 'big') + public_key.y.to_bytes(Par // 8, 'big'))
        e = int(self.hash.hash(Za + message).hex(), 16)
        t = (r + s) % self.n
        if t == 0:
            return False
        P = self.G * s + public_key * t
        if P == self.E.infinity:
            return False
        R = (e + P.x) % self.n
        return R == r


if __name__ == "__main__":
    p = int(input())
    a = int(input())
    b = int(input())
    x1, y1 = map(int, input().split())
    E = EllipticCurve(a, b, p)
    G = EllipticCurve_point((x1, y1), E)
    order = int(input())
    ID = input().encode()
    x1, y1 = map(int, input().split())
    Pa = EllipticCurve_point((x1, y1), E)
    Message = input().encode()
    Mode = input()
    if Mode == "Sign":
        da = int(input())
        k = int(input())
        SM2 = SM2(p, E, G, order)
        r, s = SM2.Sign(da, Message, 256, ID, k)
        print(r, s)
    elif Mode == "Vrfy":
        r = int(input())
        s = int(input())
        SM2 = SM2(p, E, G, order)
        print(SM2.Verify(Pa, Message, 256, ID, r, s))

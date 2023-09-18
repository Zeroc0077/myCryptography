# -*- encoding: utf-8 -*-
'''
@File    :   EIGamal.py
@Time    :   2023/05/18 16:31:54
@Author  :   zeroc 
'''
import hashlib


class ElGamal:
    def __init__(self, p: int, g: int, x: int = None, y: int = None) -> None:
        """
        Implement ElGamal Digital Signature Algorithm
        Arguments:
            p {int} -- prime number
            g {int} -- primitive root of p
            x {int} -- private key
            y {int} -- public key
        """
        self.p = p
        self.g = g
        if x:
            self.x = x
        if y:
            self.y = y

    def sign(self, k: int, m: int):
        """
        Sign the message
        Arguments:
            k {int} -- random number
            m {int} -- message
        """
        r = pow(self.g, k, self.p)
        s = (m - self.x * r) * pow(k, -1, self.p - 1) % (self.p - 1)
        return r, s

    def sign_hash(self, k: int, m: str):
        """
        Sign the message
        Arguments:
            k {int} -- random number
            m {str} -- message
        """
        m = int(hashlib.sha256(m.encode('utf-8')).hexdigest(), 16)
        r, s = self.sign(k, m)
        return r, s

    def verify(self, m: int, r: int, s: int):
        """
        Verify the message
        Arguments:
            m {int} -- message
            r {int} -- r signature
            s {int} -- s signature
            y {int} -- public key
        """
        if not (0 < r < self.p and 0 < s < self.p - 1):
            return False
        return pow(self.g, m, self.p) == (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p

    def verify_hash(self, m: str, r: int, s: int):
        """
        Verify the message
        Arguments:
            m {str} -- message
            r {int} -- r signature
            s {int} -- s signature
            y {int} -- public key
        """
        m = int(hashlib.sha256(m.encode('utf-8')).hexdigest(), 16)
        return self.verify(m, r, s)


if __name__ == "__main__":
    p = int(input())
    g = int(input())
    m = input()
    mode = input()
    if mode == 'Sign':
        x = int(input())
        k = int(input())
        eigamal = ElGamal(p, g, x=x)
        r, s = eigamal.sign_hash(k, m)
        print(r, s)
    elif mode == 'Vrfy':
        y = int(input())
        r, s = map(int, input().split())
        eigamal = ElGamal(p, g, y=y)
        print(eigamal.verify_hash(m, r, s))

# -*- encoding: utf-8 -*-
'''
@File    :   Schnorr.py
@Time    :   2023/05/25 16:22:38
@Author  :   zeroc 
'''
import hashlib


class Schnorr:
    def __init__(self, p: int, q: int, g: int, x: int = None, pk: int = None):
        """
        Implement Schnorr Digital Signature Algorithm with sha1 hash function
        Arguments:
            p {int} -- prime number
            q {int} -- prime factor of p - 1 
            g {int} -- number satisfying g^q mod p = 1
            x {int} -- private key
        """
        self.p = p
        self.q = q
        self.g = g
        self.x = x
        if x:
            self.pk = pow(g, -x, p)
        if pk:
            self.pk = pk

    def sign(self, m: str, k: int):
        """
        Sign the message
        Arguments:
            m {int} -- message
            k {int} -- random number
        """
        r = pow(self.g, k, self.p)
        e = int(hashlib.sha1((m+str(r)).encode('utf-8')).hexdigest(), 16)
        s = (k + self.x * e) % self.q
        return (e, s)

    def verify(self, m: str, e: int, s: int) -> bool:
        """
        Verify the message
        Arguments:
            m {int} -- message
            e {int} -- e signature
            s {int} -- s signature
        """
        if not (0 < e < self.q and 0 < s < self.q):
            return False
        r = (pow(self.g, s, self.p) * pow(self.pk, e, self.p)) % self.p
        e_ = int(hashlib.sha1((m+str(r)).encode('utf-8')).hexdigest(), 16)
        return e_ == e


if __name__ == "__main__":
    p = int(input())
    q = int(input())
    g = int(input())
    m = input().strip('\n')
    mode = input().strip('\n')
    if mode == 'Sign':
        x = int(input())
        k = int(input())
        schnorr = Schnorr(p, q, g, x=x)
        e, s = schnorr.sign(m, k)
        print(e, s)
    elif mode == 'Vrfy':
        pk = int(input())
        e, s = map(int, input().split(' '))
        schnorr = Schnorr(p, q, g, pk=pk)
        print(schnorr.verify(m, e, s))

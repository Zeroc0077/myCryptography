# -*- encoding: utf-8 -*-
'''
@File    :   EllipticCurve.py
@Time    :   2023/04/27 16:32:03
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
import random
from Utils.utils import *

class EllipticCurve:
    """
    construct a elliptic curve which is defined by y^2 = x^3 + ax + b (mod p) and the p is a prime number
    """
    def __init__(self, a, b, p):
        """
        Initialize the curve
        """
        if 4 * a**3 + 27 * b**2 == 0:
            raise Exception("[Error]The curve is not non-singular")
        if MillerRabinTest(p) == False:
            raise Exception("[Error]The p is not a prime number")
        self.a = a
        self.b = b
        self.p = p
        self.infinity = EllipticCurve_point((0, 0), self)

    def __str__(self) -> str:
        return "Elliptic Curve defined by y^2 = x^3 + {} * x + {} over Finite Field of size {}".format(self.a, self.b, self.p)

    def __call__(self, x, y):
        point = (x, y)
        if not self.Curve_test(point):
            raise Exception("[Error]The point is not on the curve")
        return EllipticCurve_point(point, self)

    def Curve_test(self, point):
        """
        test the point is on the curve or not
        """
        x, y = point
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def lift_x(self, x):
        """
        lift the x to the curve
        """
        try:
            y = sqrtmod(x**3 + self.a * x + self.b, self.p)
        except:
            raise Exception("[Error]There is no solution")
        return y

    def random_point(self):
        """
        generate a random point on the curve
        """
        while True:
            x = random.randint(0, self.p - 1)
            try:
                y = self.lift_x(x)
                return self(x, y)
            except:
                continue


class EllipticCurve_point:
    """
    The point on the given elliptic curve
    """

    def __init__(self, point: tuple, curve: EllipticCurve) -> None:
        self.x, self.y = point
        self.curve = curve

    def __str__(self) -> str:
        return "Point ({}, {}) on {}".format(self.x, self.y, self.curve)

    def __neg__(self):
        return EllipticCurve_point((self.x, (-self.y) % self.curve.p), self.curve)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __add__(self, other):
        if not self.curve == other.curve:
            raise Exception("[Error]The two points are not on the same curve")
        p1 = (self.x, self.y)
        p2 = (other.x, other.y)
        a, b, p = self.curve.a, self.curve.b, self.curve.p
        if p1 == (0, 0):
            return EllipticCurve_point((p2[0], p2[1]), self.curve)
        if p2 == (0, 0):
            return EllipticCurve_point((p1[0], p1[1]), self.curve)
        if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0):
            return EllipticCurve_point((0, 0), self.curve)
        if p1[0] == p2[0]:
            k = (3 * p1[0] * p1[0] + a) * inverse(2 * p1[1], p) % p
        else:
            k = (p2[1] - p1[1]) * inverse(p2[0] - p1[0], p) % p
        x = (k * k - p1[0] - p2[0]) % p
        y = (k * (p1[0] - x) - p1[1]) % p
        return EllipticCurve_point((x, y), self.curve)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, e: int):
        res = EllipticCurve_point((0, 0), self.curve)
        tmp = EllipticCurve_point((self.x, self.y), self.curve)
        while e:
            if e & 1:
                res += tmp
            e, tmp = e >> 1, tmp + tmp
        return res


def ECC_ElGamal_Encrypt(P, G, k, Public_key):
    """
    Implement the ECC ElGamal Encryption
    """
    C1 = G * k
    C2 = P + Public_key * k
    return C1, C2


def ECC_ElGamal_Decrypt(C1, C2, Private_key):
    """
    Implement the ECC ElGamal Decryption
    """
    P = C2 - C1 * Private_key
    return P


def ECC_DH(self_privte_key: int, other_public_point: EllipticCurve_point):
    """
    Implement the ECC Diffie-Hellman Key Exchange
    """
    return other_public_point * self_privte_key


if __name__ == "__main__":
    p = int(input())
    a = int(input())
    b = int(input())
    x1, y1 = map(int, input().split())
    E = EllipticCurve(a, b, p)
    G = E(x1, y1)
    op = int(input())
    if op == 1:
        x1, y1 = map(int, input().split())
        P = E(x1, y1)
        k = int(input())
        x1, y1 = map(int, input().split())
        PK = E(x1, y1)
        N = int(input())
        C1, C2 = ECC_ElGamal_Encrypt(P, G, k, PK)
        for i in range(N):
            C1, C2 = ECC_ElGamal_Encrypt(C2, G, k, PK)
        print(C1.x, C1.y)
        print(C2.x, C2.y)
    else:
        x1, y1 = map(int, input().split())
        C1 = E(x1, y1)
        x1, y1 = map(int, input().split())
        C2 = E(x1, y1)
        PK = int(input())
        N = int(input())
        P = ECC_ElGamal_Decrypt(C1, C2, PK)
        for i in range(N):
            P = ECC_ElGamal_Decrypt(C1, P, PK)
        print(P.x, P.y)
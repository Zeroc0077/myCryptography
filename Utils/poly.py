# -*- encoding: utf-8 -*-
'''
@File    :   poly.py
@Time    :   2023/03/22 09:56:19
@Author  :   zeroc 
'''
"""
Define a polynomial in 2^8 0x11b
"""


class poly:
    def __init__(self, value: int) -> None:
        """
        Initialize the polynomial class

        Properties:
        value -> the corresponding integer of the polynomial
        bin -> the binary format
        deg -> the degree of the polynomial
        """
        self.value = value
        self.bin = bin(value)[2:]
        self.deg = len(self.bin) - 1

    def __str__(self) -> str:
        """
        return the polynomial's string
        """
        res = ""
        if self.value == 0:
            return "0"
        flag = False
        for i in range(len(self.bin)):
            if self.bin[i] == "1":
                if flag == True:
                    res += "+"
                flag = True
                if i == self.deg:
                    res += "1"
                elif i == self.deg - 1:
                    res += "x"
                else:
                    res += "x^" + str(self.deg-i)
        return res

    def __add__(self, other):
        """
        Modulo 2 plus
        """
        return poly(self.value ^ other.value)

    def __sub__(self, other):
        """
        the same as the add
        """
        return poly(self.value ^ other.value)

    def __mul__(self, other):
        """
        the modulo multiplication
        """
        if self.value == 0 or other.value == 0:
            return poly(0)
        res = 0
        x, y = self.value, other.value
        while y != 0:
            if y & 1 == 1:
                res ^= x
            x <<= 1
            y >>= 1
        return poly(res) % poly(0x11b)

    def __truediv__(self, other):
        """
        Division
        """
        if other.value == 1:
            return self
        if self.deg < other.deg:
            return poly(0)
        res = 0
        x, y = self.value, other.value
        l = x.bit_length() - y.bit_length()
        while l >= 0:
            x ^= (y << l)  # ! 逐位相减
            res ^= (1 << l)  # ! 上商
            l = x.bit_length() - y.bit_length()
        return poly(res)

    def __mod__(self, other):
        """
        take Modulo
        """
        if other.value == 1:
            return poly(0)
        if self.deg < other.deg:
            return self
        res = 0
        x, y = self.value, other.value
        l = x.bit_length() - y.bit_length()
        while l >= 0:
            x ^= (y << l)  # ! 逐位相减
            res ^= (1 << l)  # ! 上商
            l = x.bit_length() - y.bit_length()
        return poly(x)

    def __pow__(self, power: int, modulo=None):
        res = poly(1)
        tmp = self
        while power != 0:
            if power & 1 == 1:
                res = res * tmp
            power >>= 1
            tmp = tmp * tmp
        return res

    def exgcd(a, b):
        if b.value == 0:
            return poly(1), poly(0), a
        x, y, z = poly.exgcd(b, a % b)
        return y, x - (a / b) * y, z

    def inverse(a):
        if a.value == 0:
            return poly(0)
        x, y, z = poly.exgcd(a, poly(0x11b))
        assert z.value == 1
        return (x) % poly(0x11b)


if __name__ == "__main__":
    # a, op, b = input().split()
    # a, b = poly(int(a, 16)), poly(int(b, 16))
    # if op == "+":
    #     print(hex((a + b).value)[2:].rjust(2, "0"))
    # elif op == "-":
    #     print(hex((a - b).value)[2:].rjust(2, "0"))
    # elif op == "*":
    #     print(hex((a * b).value)[2:].rjust(2, "0"))
    # elif op == "/":
    #     res, rem = a / b, a % b
    #     print(hex(res.value)[2:].rjust(2, "0"), hex(rem.value)[2:].rjust(2, "0"))
    # m, e = input().split()
    # m, e = poly(int(m, 16)), int(e)
    # res = m ** e
    # print(hex(res.value)[2:].rjust(2, "0"))
    # x, y = input().split()
    # x, y = poly(int(x, 16)), poly(int(y, 16))
    # a, b, gcd = poly.exgcd(x, y)
    # print(hex(a.value)[2:].rjust(2, "0"), hex(b.value)[2:].rjust(2, "0"), hex(gcd.value)[2:].rjust(2, "0"))
    x = poly(int(input(), 16))
    res = poly.inverse(x)
    print(hex(res.value)[2:].rjust(2, "0"))

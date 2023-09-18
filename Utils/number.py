# -*- encoding: utf-8 -*-
'''
@File    :   number.py
@Time    :   2023/06/08 15:58:32
@Author  :   zeroc 
'''
import sys
import struct


def Exgcd(a, b):
    """
    实现扩展的欧几里得算法

    参数：
    a, b -> 给定的两个数

    返回值：
    x -> a, b中较大数所对应的系数, 要求其为满足条件的最小正整数
    y -> a, b中较小数所对应的系数
    gcd -> a, b两数的最大公因数
    """
    flag = 0  # ! flag标志是否进行交换
    if abs(a) < abs(b):  # ! 根据绝对值大小决定是否进行交换
        m, n = b, a
        flag = 1
    else:
        m, n = a, b
    if n == 0:  # ! 0与任何数的最大公因子就是该数
        if flag:
            return 0, 1, m
        else:
            return 1, 0, m
    x1, y1 = 1, 0
    x2, y2 = 0, 1
    r = m % n
    while True:
        """
        使用矩阵进行相消直至两个行向量的第三项整除
        """
        if r == 0:
            x, y, gcd = x2, y2, n
            break
        q = m // n
        t1, t2, t3 = x1 - q * x2, y1 - q * y2, m - q * n
        x1, y1, m = x2, y2, n
        x2, y2, n = t1, t2, t3
        r = m % n
    if gcd < 0:  # ! 如果输入包含负数会出现gcd为负数的情况, 需要同时乘上-1
        x, y, gcd = -x, -y, -gcd
    if flag == 1:  # ! 如果进行了交换需要交换回来
        x, y = y, x
    while x <= 0:  # ! 根据通解得到x为最小正整数时的y
        x += abs(b) // gcd
        y = (gcd - a * x) // b
    return x, y, gcd


def inverse(a, b):
    """
    实现求逆元算法

    参数：
    a, b -> 输入给定的两数

    返回值：
    a 在模 b 意义下的逆元
    """
    test = Exgcd(a, b)[2]
    if test != 1:
        raise ValueError("a and b are not relatively prime")
    return Exgcd(a, b)[0]


def qpow(m, e, n):
    """
    实现快速模幂算法

    参数：
    m -> 底数
    e -> 指数
    n -> 模数

    返回值：
    c -> m^e % n的结果
    """
    c = 1
    while e != 0:
        if e & 1 == 1:
            c = (c * m) % n
        e >>= 1
        m = (m * m) % n
    return c


def long_to_bytes(n, blocksize=0):
    if n < 0 or blocksize < 0:
        raise ValueError("Values must be non-negative")

    result = []
    pack = struct.pack

    bsr = blocksize
    while bsr >= 8:
        result.insert(0, pack('>Q', n & 0xFFFFFFFFFFFFFFFF))
        n = n >> 64
        bsr -= 8

    while bsr >= 4:
        result.insert(0, pack('>I', n & 0xFFFFFFFF))
        n = n >> 32
        bsr -= 4

    while bsr > 0:
        result.insert(0, pack('>B', n & 0xFF))
        n = n >> 8
        bsr -= 1

    if n == 0:
        if len(result) == 0:
            bresult = b'\x00'
        else:
            bresult = b''.join(result)
    else:
        while n > 0:
            result.insert(0, pack('>Q', n & 0xFFFFFFFFFFFFFFFF))
            n = n >> 64
        result[0] = result[0].lstrip(b'\x00')
        bresult = b''.join(result)
        if blocksize > 0:
            target_len = ((len(bresult) - 1) // blocksize + 1) * blocksize
            bresult = b'\x00' * (target_len - len(bresult)) + bresult

    return bresult


def bytes_to_long(s):
    acc = 0
    unpack = struct.unpack
    if sys.version_info[0:3] < (2, 7, 4):
        if isinstance(s, bytearray):
            s = bytes(s)
        elif isinstance(s, memoryview):
            s = s.tobytes()
    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = b'\x00' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc


def unpad(padded_data, block_size, style='pkcs7'):

    pdata_len = len(padded_data)
    if pdata_len == 0:
        raise ValueError("Zero-length input cannot be unpadded")
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = padded_data[-1]
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:] != bytes([padding_len])*padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1] != bytes([0])*(padding_len-1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bytes([128]))
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len > 1 and padded_data[1-padding_len:] != bytes([0])*(padding_len-1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]

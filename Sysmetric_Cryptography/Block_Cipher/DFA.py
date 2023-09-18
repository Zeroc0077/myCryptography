# -*- encoding: utf-8 -*-
'''
@File    :   DFA.py
@Time    :   2023/04/03 19:17:30
@Author  :   zeroc 
'''
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36
)


def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])


def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i + 4]) for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    result = []
    for i in matrix:
        for j in i:
            result.append(j)
    return result


def xtime(a): return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def getdiff(a, b):
    """
    get output difference from input
    """
    return s_box[a] ^ s_box[b]


def get_inputdiff(diff, times):
    """
    get the input diff sequence
    """
    zlist = []
    for z in range(256):
        for y in range(256):
            if times == 2:
                tmp = xtime(z)
            elif times == 3:
                tmp = z ^ xtime(z)
            else:
                tmp = z
            if getdiff(y, y ^ tmp) == diff:
                zlist.append(z)
    return set(zlist)


def get_zlist(diffs, times):
    """
    get the intersection of the zlist
    """
    return set.intersection(get_inputdiff(diffs[0], times[0]), get_inputdiff(diffs[1], times[1]), get_inputdiff(diffs[2], times[2]), get_inputdiff(diffs[3], times[3]))


def get_ylist(zlist, diff, times):
    """
    according to the zlist and diff, get the ylist
    """
    ylist = []
    for z in zlist:
        for y in range(256):
            if times == 2:
                tmp = xtime(z)
            elif times == 3:
                tmp = z ^ xtime(z)
            else:
                tmp = z
            if getdiff(y, y ^ tmp) == diff:
                ylist.append(y)
    return set(ylist)


def get_intersection(y):
    tmp = set({i for i in range(256)})
    for i in y:
        tmp = tmp & i
    return tmp


def attack(ct, error, times):
    index = 0
    y = []
    for er in error:
        loc = (index % 40) // 10
        if loc == 0:
            diffs = [ct[0][0] ^ er[0][0], ct[1][3] ^ er[1]
                     [3], ct[2][2] ^ er[2][2], ct[3][1] ^ er[3][1]]
        if loc == 1:
            diffs = [ct[0][1] ^ er[0][1], ct[1][0] ^ er[1]
                     [0], ct[2][3] ^ er[2][3], ct[3][2] ^ er[3][2]]
        if loc == 2:
            diffs = [ct[0][2] ^ er[0][2], ct[1][1] ^ er[1]
                     [1], ct[2][0] ^ er[2][0], ct[3][3] ^ er[3][3]]
        if loc == 3:
            diffs = [ct[0][3] ^ er[0][3], ct[1][2] ^ er[1]
                     [2], ct[2][1] ^ er[2][1], ct[3][0] ^ er[3][0]]
        zlist = get_zlist(diffs, times[(index % 40) // 10])
        for i in range(4):
            y.append(get_ylist(zlist, diffs[i], times[(index % 40) // 10][i]))
        index += 1
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    y7 = []
    y8 = []
    y9 = []
    y10 = []
    y11 = []
    y12 = []
    y13 = []
    y14 = []
    y15 = []
    for i in range(10):
        y0.append(y[4*i])
        y7.append(y[4*i+1])
        y10.append(y[4*i+2])
        y13.append(y[4*i+3])
        y1.append(y[4*i+40])
        y4.append(y[4*i+41])
        y11.append(y[4*i+42])
        y14.append(y[4*i+43])
        y2.append(y[4*i+80])
        y5.append(y[4*i+81])
        y8.append(y[4*i+82])
        y15.append(y[4*i+83])
        y3.append(y[4*i+120])
        y6.append(y[4*i+121])
        y9.append(y[4*i+122])
        y12.append(y[4*i+123])
    Y = []
    for i in range(16):
        tmp = eval("get_intersection(y{index})".format(index=i))
        Y.append(s_box[list(tmp)[0]])
    lastkey = xor(Y, matrix2bytes(ct))
    return int.from_bytes(lastkey, byteorder="big")


def g(a):
    """
    reverse the expand key when i mod 4 == 0
    """
    a = ((a << 8 & 0xffffffff) + (a >> 24 & 0xff))
    res = s_box[a >> 24 & 0xff] << 24
    res += s_box[a >> 16 & 0xff] << 16
    res += s_box[a >> 8 & 0xff] << 8
    res += s_box[a & 0xff]
    return res


def RecoverKey(lastkey):
    """
    inverse the key expansion
    """
    res = 0
    key = [lastkey >> 96, lastkey >> 64 & 0xffffffff,
           lastkey >> 32 & 0xffffffff, lastkey & 0xffffffff]
    for i in range(10):
        key[-1] = key[-1] ^ key[-2]
        key[-2] = key[-2] ^ key[-3]
        key[-3] = key[-3] ^ key[-4]
        key[-4] = key[-4] ^ g(key[-1]) ^ (r_con[::-1][i] << 24)
    for i in range(4):
        res += key[i] << (32 * (3 - i))
    return res


if __name__ == "__main__":
    pt = bytes2matrix(bytes.fromhex(input().strip()[2:]))
    ct = bytes2matrix(bytes.fromhex(input().strip()[2:]))
    error = []
    for _ in range(160):
        error.append(bytes2matrix(bytes.fromhex(input().strip()[2:])))
    times = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    lastkey = attack(ct, error[:40], times)
    key = RecoverKey(lastkey)
    print(hex(key))

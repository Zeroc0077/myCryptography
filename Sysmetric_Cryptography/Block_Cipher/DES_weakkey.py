# -*- encoding: utf-8 -*-
'''
@File    :   DES_weakkey.py
@Time    :   2023/03/16 17:03:04
@Author  :   zeroc 
'''
pc1 = [57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
       10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
       14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4]

inv_pc1 = [8, 16, 24, 56, 52, 44, 36, 7, 15, 23, 55, 51, 43, 35,
           6, 14, 22, 54, 50, 42, 34, 5, 13, 21, 53, 49, 41, 33,
           4, 12, 20, 28, 48, 40, 32, 3, 11, 19, 27, 47, 39, 31,
           2, 10, 18, 26, 46, 38, 30, 1, 9, 17, 25, 45, 37, 29]
subkey = ["0000000000000000000000000000", "1111111111111111111111111111", "0101010101010101010101010101", "1010101010101010101010101010"]
#! inverse PC1
def inv_PC1(a):
    res = ""
    j = 0
    for i in range(64):
        if i % 8 == 7:
            res += "0"
            j += 1
        else:    
            res += a[inv_pc1[i-j]-1]
    return res
#! weak key
def generate_key():
    for i in range(2):
        for j in range(2):
            res = ""
            s = subkey[i] + subkey[j]
            s = inv_PC1(s)
            for k in range(8):
                tmp = s[k*8:(k+1)*8-1]
                if tmp.count('1') % 2 == 0:
                    tmp = tmp + '1'
                else:
                    tmp = tmp + '0'
                res += tmp
            print("0x" + hex(int(res, 2))[2:].rjust(16, "0"))

    for i in range(2):
        for j in range(2):
            res = ""
            s = subkey[i] + subkey[j]
            s = inv_PC1(s)
            for k in range(8):
                tmp = s[k*8:(k+1)*8-1]
                if tmp.count('1') % 2 == 0:
                    tmp = tmp + '0'
                else:
                    tmp = tmp + '1'
                res += tmp
            print("0x" + hex(int(res, 2))[2:].rjust(16, "0"))
    #! Semi-weak key
    cmp = []
    for i in range(4):
        for j in range(4):
            if i <= 1 and j <= 1:
                continue
            res = ""
            s = subkey[i] + subkey[j]
            s = inv_PC1(s)
            for k in range(8):
                tmp = s[k*8:(k+1)*8-1]
                if tmp.count('1') % 2 == 0:
                    tmp = tmp + '1'
                else:
                    tmp = tmp + '0'
                res += tmp
            res = hex(int(res, 2))[2:].rjust(16, "0")
            if cmp.count(res) == 0:
                print("0x" + res, "0x" + res[2:4]+res[:2]+res[6:8]+res[4:6]+res[10:12]+res[8:10]+res[14:16]+res[12:14])
            cmp.append(res)
            cmp.append(res[2:4]+res[:2]+res[6:8]+res[4:6]+res[10:12]+res[8:10]+res[14:16]+res[12:14])

    cmp = []
    for i in range(4):
        for j in range(4):
            if i <= 1 and j <= 1:
                continue
            res = ""
            s = subkey[i] + subkey[j]
            s = inv_PC1(s)
            for k in range(8):
                tmp = s[k*8:(k+1)*8-1]
                if tmp.count('1') % 2 == 0:
                    tmp = tmp + '0'
                else:
                    tmp = tmp + '1'
                res += tmp
            res = hex(int(res, 2))[2:].rjust(16, "0")
            if cmp.count(res) == 0:
                print("0x" + res, "0x" + res[2:4]+res[:2]+res[6:8]+res[4:6]+res[10:12]+res[8:10]+res[14:16]+res[12:14])
            cmp.append(res)
            cmp.append(res[2:4]+res[:2]+res[6:8]+res[4:6]+res[10:12]+res[8:10]+res[14:16]+res[12:14])

if __name__ == "__main__":
    generate_key()
# -*- encoding: utf-8 -*-
'''
@File    :   Miller_Rabin.py
@Time    :   2023/02/23 19:30:57
@Author  :   zeroc 
'''
import sys
sys.path.append(".")
import random

def MillerRabinTest(n, k):
    """
    实现Miller-Rabin素性检测算法
    """
    if n == 2:  #! 特判2
        return True
    elif n & 1 == 0:  #! n为偶数
        return False
    else:
        k = 0
        q = n - 1
        flag = True
        while True:  #! 将n - 1分解为2^k * q
            q = q // 2
            k += 1
            if q % 2 == 1:
                break
        for _ in range(k):  #! 设定检测次数
            a = random.randint(2, n - 1)  #! 随机选择(2, n-1)之间的一个整数
            x = pow(a, q, n)  #! 计算a^q % n
            if x == 1 or x == n - 1:
                continue
            else:
                for _ in range(k):
                    x = x * x % n
                    if x == n - 1:
                        flag = True
                        break
                    else:
                        flag = False
    return flag


if __name__ == "__main__":
    flag = MillerRabinTest(int(input()))
    if flag:
        print("YES")
    else:
        print("NO")

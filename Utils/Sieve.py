# -*- encoding: utf-8 -*-
'''
@File    :   Sieve.py
@Time    :   2023/02/23 22:20:04
@Author  :   zeroc 
'''
def filter_prime(n) -> list:
    """
    实现厄拉多筛法：给出小于n的所有素数

    这里对厄拉多筛法进行优化
    """
    if n < 2:  #! 没有小于2的素数
        return None
    if n == 2:  #! 特判2
        return [2]
    end = (n - 3) // 2  #! 这里不考虑2的倍数即偶数, 将i映射为2*i + 3
    is_prime = [True for _ in range(end + 1)]  #! 标记数组初始化为True
    for i in range(3, int(pow(n, 0.5)) + 1, 2):  #! 判断小于根号n的奇数的倍数即可
        k = (i - 3) // 2
        if is_prime[k]:
            for j in range(i * i, n + 1, 2 * i):
                is_prime[(j - 3) // 2] = False
    return [2] + [2 * i + 3 for i in range(end + 1) if is_prime[i]]


if __name__ == "__main__":
    n = int(input())
    for i in filter_prime(n):
        print(i, end=" ")
# -*- encoding: utf-8 -*-
'''
@File    :   MT19937.py
@Time    :   2023/04/04 22:27:30
@Author  :   zeroc 
'''


class MT19937:
    # initialize the state from a seed
    def __init__(self, seed: int) -> None:
        self.MT = [0] * 624
        self.index = 0
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = (0xffffffff & (
                0x6c078965 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i))

    # extract pseudorandom number
    def extract_number(self):
        if self.index == 0:
            self.twist()
        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9d2c5680)
        y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ (y >> 18)
        self.index = (self.index + 1) % 624
        return y & 0xffffffff

    # twist the state
    def twist(self):
        for i in range(0, 624):
            y = 0xffffffff & (
                (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff))
            self.MT[i] = (y >> 1) ^ self.MT[(i + 397) % 624]
            if y % 2 != 0:
                self.MT[i] = self.MT[i] ^ 0x9908b0df


if __name__ == "__main__":
    seed = int(input())
    mt = MT19937(seed)
    for i in range(20):
        print(mt.extract_number())

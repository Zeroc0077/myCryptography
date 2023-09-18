# -*- encoding: utf-8 -*-
'''
@File    :   LCG.py
@Time    :   2023/06/27 12:01:34
@Author  :   zeroc 
'''
from Crypto.Util.number import *
from functools import *
class LCG:
    def __init__(self, a: int, b: int, m: int, seed: int) -> None:
        self.a = a
        self.b = b
        self.m = m
        self.seed = seed

    def next(self) -> int:
        self.seed = (self.a * self.seed + self.b) % self.m
        return self.seed

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * \
        inverse(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1,
              t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)


if __name__ == "__main__":
    enc = 1394750987633511196198073798293968299270362535855266248728183586194775921337118865951859025
    state = [351432794845593565103371410729044421045900121196509173454394951376703279283683542964750048, 956383696685631568345966539418806242572293863822471004691811405173627598657922792811890606, 68111317663342845874067402660097869512716284793855015129268734708469129702843728321432716, 55753231408394505146272704565372027859908328762573966393544177986196995023441014119579519, 1624650311933644661853686470295998309394002786041378280760209450755683221865700588801446730, 1276247570363282543513133463876874351009647962012676390920220466912282389481640381213092596]
    modulus, multiplier, increment = crack_unknown_modulus(state)
    lcg = LCG(multiplier, increment, modulus, state[0])
    xorstate = 0
    for i in range(99):
        xorstate = lcg.next()
    flag = xorstate ^ enc
    print(long_to_bytes(flag))
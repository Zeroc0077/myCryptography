# -*- encoding: utf-8 -*-
'''
@File    :   letter_frequency_attack.py
@Time    :   2023/03/06 17:34:45
@Author  :   zeroc 
'''
dic = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0,
       "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0,
       "y": 0, "z": 0}


def frequency_attack(text: str):
    for i in text:
        dic[i] += 1
    Max = max(dic.values())
    for i in list(dic.keys()):
        if dic[i] == Max:
            print((ord(i) - ord('e')) % 26)
            return dic


if __name__ == "__main__":
    text = "fmhc ni abc mgc abngr abea asegiqcgpi anjc egp iueqc".replace(
        " ", "")
    frequency_attack(text)
    print(dic)

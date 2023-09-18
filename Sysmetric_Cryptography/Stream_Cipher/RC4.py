# -*- encoding: utf-8 -*-
'''
@File    :   RC4.py
@Time    :   2023/03/27 10:18:21
@Author  :   zeroc 
'''
class RC4:
    #! init Rc4 class
    def __init__(self, key: bytes):
        self.key = key

    #! generate S_box
    def get_S(self):
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + self.key[i % len(self.key)]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    #! apply rc4 algorithm
    def rc4(self, text: bytes):
        S = self.get_S()
        i = j = 0
        out = []
        for char in text:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            out.append(char ^ S[(S[i] + S[j]) % 256])
        return bytes(out)

    #! encrypt
    def encrypt(self, text: bytes):
        return self.rc4(text)

    #! decrypt
    def decrypt(self, text: bytes):
        return self.rc4(text)

if __name__ == "__main__":
    # key = bytes.fromhex(input().strip()[2:])
    # text = bytes.fromhex(input().strip()[2:])
    # rc4 = RC4(key)
    # cipher = rc4.encrypt(text)
    # print("0x" + cipher.hex())
    key = b'583908295080'
    text = b'APIKEY'
    rc4 = RC4(key)
    cipher = rc4.encrypt(text)
    print("0x" + cipher.hex())
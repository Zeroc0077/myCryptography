# -*- encoding: utf-8 -*-
'''
@File    :   SM4.py
@Time    :   2023/03/27 10:28:34
@Author  :   zeroc 
'''
FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]

Sbox = [
    [0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7,
     0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
    [0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3,
     0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
    [0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a,
     0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
    [0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95,
     0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
    [0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba,
     0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
    [0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b,
     0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
    [0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2,
     0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
    [0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52,
     0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
    [0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5,
     0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
    [0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55,
     0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
    [0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60,
     0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
    [0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f,
     0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
    [0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f,
     0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
    [0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd,
     0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
    [0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e,
     0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
    [0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20,
     0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]
]

CK = [0x70e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9, 0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
      0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299, 0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]


class SM4:
    #! initialize SM4 with key
    def __init__(self, key: bytes, iv: bytes = None) -> None:
        self.key = key
        self.iv = iv
        self.K = self.KeyExpansion()

    #! S_box permutation
    def S(self, A: int) -> int:
        return Sbox[A >> 4][A & 0xf]

    #! unlinear transformation
    def tau(self, A: int) -> int:
        res = 0
        res += self.S(A >> 24) << 24
        res += self.S(A >> 16 & 0xff) << 16
        res += self.S(A >> 8 & 0xff) << 8
        res += self.S(A & 0xff)
        return res

    #! left rotate
    def left_rotate(self, A: int, n: int) -> int:
        return ((A << n) | (A >> (32 - n))) & 0xffffffff

    #! linear transformation 1
    def L1(self, A: int) -> int:
        return A ^ self.left_rotate(A, 2) ^ self.left_rotate(A, 10) ^ self.left_rotate(A, 18) ^ self.left_rotate(A, 24)

    #! linear transformation 2 used in key expansion
    def L2(self, A: int) -> int:
        return A ^ self.left_rotate(A, 13) ^ self.left_rotate(A, 23)

    #! T transformation
    def T1(self, A: int) -> int:
        return self.L1(self.tau(A))
    
    #! T transformation
    def T2(self, A: int) -> int:
        return self.L2(self.tau(A))

    #! key expansion
    def KeyExpansion(self):
        K = [0] * 36
        MK = [0] * 4
        for i in range(4):
            MK[i] = int.from_bytes(self.key[i * 4:i * 4 + 4], 'big')
        K[0] = MK[0] ^ FK[0]
        K[1] = MK[1] ^ FK[1]
        K[2] = MK[2] ^ FK[2]
        K[3] = MK[3] ^ FK[3]
        for i in range(32):
            K[i + 4] = K[i] ^ self.T2(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ CK[i])
        return K[4:]
    
    #! F function
    def F(self, X: list, rk: int) -> int:
        return X[0] ^ self.T1(X[1] ^ X[2] ^ X[3] ^ rk)
    
    #! encryption
    def encrypt(self, plaintext: bytes) -> bytes:
        X = [0] * 36
        for i in range(4):
            X[i] = int.from_bytes(plaintext[i * 4:i * 4 + 4], 'big')
        for i in range(32):
            X[i + 4] = self.F(X[i:i + 4], self.K[i])
        ciphertext = b''
        for i in range(4):
            ciphertext += X[35 - i].to_bytes(4, 'big')
        return ciphertext
    
    #! decryption
    def decrypt(self, ciphertext: bytes) -> bytes:
        X = [0] * 36
        for i in range(4):
            X[i] = int.from_bytes(ciphertext[i * 4:i * 4 + 4], 'big')
        for i in range(32):
            X[i + 4] = self.F(X[i:i + 4], self.K[31 - i])
        plaintext = b''
        for i in range(4):
            plaintext += X[35 - i].to_bytes(4, 'big')
        return plaintext

    #! padding
    def PKCS7_Padding(self, plaintext: bytes) -> bytes:
        padding_len = 16 - len(plaintext) % 16
        return plaintext + bytes([padding_len] * padding_len)

    #! remove padding
    def PKCS7_Unpadding(self, plaintext: bytes) -> bytes:
        padding_len = plaintext[-1]
        for i in plaintext[-padding_len:]:
            if i != padding_len:
                return plaintext
        return plaintext[:-padding_len]

    #! SM4_ECB_encryption
    def ECB_encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = b''
        plaintext = self.PKCS7_Padding(plaintext)
        for i in range(0, len(plaintext), 16):
            ciphertext += self.encrypt(plaintext[i:i + 16])
        return ciphertext
    
    #! SM4_ECB_decryption
    def ECB_decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = b''
        for i in range(0, len(ciphertext), 16):
            plaintext += self.decrypt(ciphertext[i:i + 16])
        return self.PKCS7_Unpadding(plaintext)
    
    #! SM4_CBC_encryption
    def CBC_encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = b''
        plaintext = self.PKCS7_Padding(plaintext)
        for i in range(0, len(plaintext), 16):
            plaintext_block = plaintext[i:i + 16]
            if i == 0:
                plaintext_block = bytes([plaintext_block[j] ^ self.iv[j] for j in range(16)])
            else:
                plaintext_block = bytes([plaintext_block[j] ^ ciphertext[i + j - 16] for j in range(16)])
            ciphertext += self.encrypt(plaintext_block)
        return ciphertext
    
    #! SM4_CBC_decryption
    def CBC_decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = b''
        for i in range(0, len(ciphertext), 16):
            ciphertext_block = ciphertext[i:i + 16]
            plaintext_block = self.decrypt(ciphertext_block)
            if i == 0:
                plaintext_block = bytes([plaintext_block[j] ^ self.iv[j] for j in range(16)])
            else:
                plaintext_block = bytes([plaintext_block[j] ^ ciphertext[i + j - 16] for j in range(16)])
            plaintext += plaintext_block
        return self.PKCS7_Unpadding(plaintext)

    #! SM4_CTR_encryption
    def CTR_encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = b''
        counter = 0
        for i in range(0, len(plaintext), 16):
            plaintext_block = plaintext[i:i + 16]
            key_block = self.encrypt((int.from_bytes(self.iv, 'big') + counter).to_bytes(16, 'big'))
            counter += 1
            ciphertext += bytes([plaintext_block[j] ^ key_block[j] for j in range(len(plaintext_block))])
        return ciphertext
    
    #! SM4_CTR_decryption
    def CTR_decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = b''
        counter = 0
        for i in range(0, len(ciphertext), 16):
            ciphertext_block = ciphertext[i:i + 16]
            key_block = self.encrypt((int.from_bytes(self.iv, 'big') + counter).to_bytes(16, 'big'))
            counter += 1
            plaintext += bytes([ciphertext_block[j] ^ key_block[j] for j in range(len(ciphertext_block))])
        return plaintext
    
    #! SM4_CFB_encryption
    #! the block size is the value of the offset
    def CFB_encrypt(self, plaintext: bytes, offset: int=7) -> bytes:
        ciphertext = b''
        FB = self.iv
        for i in range(0, len(plaintext), offset):
            plaintext_block = plaintext[i:i + offset]
            key_block = self.encrypt(FB)
            ciphertext_block = bytes([plaintext_block[j] ^ key_block[j] for j in range(len(plaintext_block))])
            ciphertext += ciphertext_block
            FB = (((int.from_bytes(FB, "big") << offset * 8) & (2 ** 128 - 1)) + int.from_bytes(ciphertext_block, "big")).to_bytes(16, "big")
        return ciphertext
    
    #! SM4_CFB_decryption
    #! the block size is the value of the offset
    def CFB_decrypt(self, ciphertext: bytes, offset: int=7) -> bytes:
        plaintext = b''
        FB = self.iv
        for i in range(0, len(ciphertext), offset):
            ciphertext_block = ciphertext[i:i + offset]
            key_block = self.encrypt(FB)
            plaintext_block = bytes([ciphertext_block[j] ^ key_block[j] for j in range(len(ciphertext_block))])
            plaintext += plaintext_block
            FB = (((int.from_bytes(FB, "big") << offset * 8) & (2 ** 128 - 1)) + int.from_bytes(ciphertext_block, "big")).to_bytes(16, "big")
        return plaintext
    
    #! SM4_OFB_encryption
    #! the block size is the value of the offset
    def OFB_encrypt(self, plaintext: bytes, offset: int=7) -> bytes:
        ciphertext = b''
        FB = self.iv
        for i in range(0, len(plaintext), offset):
            plaintext_block = plaintext[i:i + offset]
            key_block = self.encrypt(FB)
            ciphertext_block = bytes([plaintext_block[j] ^ key_block[j] for j in range(len(plaintext_block))])
            ciphertext += ciphertext_block
            FB = (((int.from_bytes(FB, "big") << offset * 8) & (2 ** 128 - 1)) + (int.from_bytes(key_block, "big") >> (128 - offset * 8))).to_bytes(16, "big")
        return ciphertext
    
    #! SM4_OFB_decryption
    #! the block size is the value of the offset
    def OFB_decrypt(self, ciphertext: bytes, offset: int=7) -> bytes:
        plaintext = b''
        FB = self.iv
        for i in range(0, len(ciphertext), offset):
            ciphertext_block = ciphertext[i:i + offset]
            key_block = self.encrypt(FB)
            plaintext += bytes([ciphertext_block[j] ^ key_block[j] for j in range(len(ciphertext_block))])
            FB = (((int.from_bytes(FB, "big") << offset * 8) & (2 ** 128 - 1)) + (int.from_bytes(key_block, "big") >> (128 - offset * 8))).to_bytes(16, "big")
        return plaintext

if __name__ == "__main__":
    with open("pic_original.bmp", "rb") as f:
        plaintext = f.read()
        head = plaintext[:54]
        plaintext = plaintext[54:]
        key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x0a\x0b\x0c\x0d\x0e\x0f'
        iv = key    
        sm4 = SM4(key, iv)
        ciphertext = sm4.CBC_encrypt(plaintext)
        with open("pic_CBC_encrypt.bmp", "wb") as f:
            f.write(head + ciphertext)
            print("CBC encryption completed")
    with open("pic_original.bmp", "rb") as f:
        plaintext = f.read()
        head = plaintext[:54]
        plaintext = plaintext[54:]
        key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x0a\x0b\x0c\x0d\x0e\x0f'
        sm4 = SM4(key)
        ciphertext = sm4.ECB_encrypt(plaintext)
        with open("pic_ECB_encrypt.bmp", "wb") as f:
            f.write(head + ciphertext)
            print("ECB encryption completed")
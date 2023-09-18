# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/05/25 16:08:39
@Author  :   zeroc 
'''
import sys
import os
sys.dont_write_bytecode = True
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)
from Sysmetric_Cryptography.Block_Cipher.SM4 import *
from Sysmetric_Cryptography.Block_Cipher.DES import *
from Sysmetric_Cryptography.Block_Cipher.AES import *
from DigitalSignature.Schnorr import *
from DigitalSignature.EIGamal import *
from RSA.RSA import *
from Hash.SM3 import *
from Hash.SHA1 import *
from Utils.utils import *
Prompts = "\033[0;33mλ CryptoWheel → \033[0m"


def start():
    tmp = input(Prompts)
    if tmp != "start":
        print("\033[0;31m[+]Invalid Command\033[0m")
        exit(1)


def menu():
    print("[+]Here are implemented modules")
    print(
        """
   |---------------------------------------------|
   | 1.  Miller Rabin Test                       |
   | 2.  Quick Pow                               |
   | 3.  Int2Text                                |
   | 4.  Text2Int                                |
   | 5.  Inverse                                 |
   | 6.  SHA1                                    |
   | 7.  SM3                                     |
   | 8.  ElGamal                                 |
   | 9.  AES Encrypt                             |
   | 10. AES Decrypt                             |
   | 11. DES Encrypt                             |
   | 12. DES Decrypt                             |
   | 13. SM4 Encrypt                             |
   | 14. SM4 Decrypt                             |
   | 15. SM4 Encrypt (FILE)                      |
   | 16. SM4 Decrypt (FILE)                      |
   | 17. RSA Encrypt                             |
   | 18. RSA Decrypt                             |
   |---------------------------------------------|
   """
    )
    print("[+]Type the number to choose one module")


def get_choice():
    choice = input(Prompts)
    try:
        return int(choice)
    except:
        print("\033[0;31m[+]Invalid Number\033[0m")
        exit(1)


def _Miller_Rabin_Test():
    n = int(input("[MRT]Please Input the Test Number: "))
    k = int(input("[MRT]Please Input the Test Times: "))
    res = MillerRabinTest(n, k)
    if res:
        print("\033[0;32m[MRT]YES\033[0m")
    else:
        print("\033[0;31m[MRT]NO\033[0m")
    exit(0)


def _Quick_Pow():
    m = int(input("[Qpow]Please Input the Base: "))
    e = int(input("[Qpow]Please Input the Exponent: "))
    n = int(input("[Qpow]Please Input the Modulus: "))
    res = qpow(m, e, n)
    print("\033[0;32m[Qpow]Result: %d\033[0m" % res)
    exit(0)


def _Int2Text():
    number = int(input("[+]Please Input the Number: "))
    res = long_to_bytes(number)
    print("\033[0;32m[+]Result: %s\033[0m" % res)
    exit(0)


def _Text2Int():
    text = input("[+]Please Input the Text: ")
    res = bytes_to_long(text.encode())
    print("\033[0;32m[+]Result: %d\033[0m" % res)
    exit(0)


def _Inverse():
    a = int(input("[Inv]Please Input the Number: "))
    n = int(input("[Inv]Please Input the Modulus: "))
    try:
        res = inverse(a, n)
    except:
        print("\033[0;31m[Inv]Not relatively prime\033[0m")
        exit(1)
    print("\033[0;32m[Inv]Result: %d\033[0m" % res)
    exit(0)


def _SHA1():
    text = input("[SHA1]Please Input the Text: ")
    sha1 = SHA1()
    res = sha1.hash(text.encode()).hex()
    print("\033[0;32m[SHA1]Result: %s\033[0m" % res)
    exit(0)


def _SM3():
    text = input("[SM3]Please Input the Text: ")
    sm3 = SM3()
    res = sm3.hash(text.encode()).hex()
    print("\033[0;32m[SM3]Result: %s\033[0m" % res)
    exit(0)


def _ElGamal():
    mode = input("[ElGamal]Please Input the Mode (Sign/Verify): ")
    if mode != "Sign" and mode != "Verify":
        print("\033[0;31m[EiGamal]Invalid Mode\033[0m")
        exit(1)
    if mode == "Sign":
        p = int(input("[ElGamal]Please Input the Prime Number: "))
        if not MillerRabinTest(p, 10):
            print("\033[0;31m[ElGamal]Invalid Prime Number\033[0m")
            exit(1)
        g = int(input("[ElGamal]Please Input the Generator: "))
        x = int(input("[ElGamal]Please Input the Private Key: "))
        k = int(input("[ElGamal]Please Input the Random Number: "))
        m = input("[ElGamal]Please Input the Message: ")
        elgamal = ElGamal(p, g, x=x)
        res = elgamal.sign_hash(k, m)
        print("\033[0;32m[ElGamal]Result: %s\033[0m" % str(res))
        exit(0)
    else:
        p = int(input("[ElGamal]Please Input the Prime Number: "))
        if not MillerRabinTest(p, 10):
            print("\033[0;31m[ElGamal]Invalid Prime Number\033[0m")
            exit(1)
        g = int(input("[ElGamal]Please Input the Generator: "))
        y = int(input("[ElGamal]Please Input the Public Key: "))
        m = input("[ElGamal]Please Input the Message: ")
        r = int(input("[ElGamal]Please Input the r: "))
        s = int(input("[ElGamal]Please Input the s: "))
        elgamal = ElGamal(p, g, y=y)
        res = elgamal.verify_hash(m, r, s)
        if res:
            print("\033[0;32m[ElGamal]YES\033[0m")
        else:
            print("\033[0;31m[ElGamal]NO\033[0m")
        exit(0)


def _AES_Encrypt():
    key = input("[AES]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[AES]Invalid Key Length\033[0m")
        exit(1)
    try:
        key = bytes.fromhex(key)
    except:
        print("\033[0;31m[AES]Invalid Key Format\033[0m")
        exit(1)
    aes = AES(key)
    text = input("[AES]Please Input the Text: ")
    res = aes.AES_encrypt("AES_ECB", text.encode()).hex()
    print("\033[0;32m[AES]Result(in hex): %s\033[0m" % res)
    exit(0)


def _AES_Decrypt():
    key = input("[AES]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[AES]Invalid Key Length\033[0m")
        exit(1)
    try:
        key = bytes.fromhex(key)
    except:
        print("\033[0;31m[AES]Invalid Key Format\033[0m")
        exit(1)
    aes = AES(key)
    text = input("[AES]Please Input the Text(in hex): ")
    try:
        text = bytes.fromhex(text)
    except:
        print("\033[0;31m[AES]Invalid Text Format\033[0m")
        exit(1)
    res = aes.AES_decrypt("AES_ECB", text)
    res = unpad(res, 16)
    print("\033[0;32m[AES]Result: %s\033[0m" % res)
    exit(0)


def _DES_Encrypt():
    key = input("[DES]Please Input the Key(in hex): ")
    if len(key) != 16:
        print("\033[0;31m[DES]Invalid Key Length\033[0m")
        exit(1)
    try:
        key = int(key, 16)
    except:
        print("\033[0;31m[DES]Invalid Key Format\033[0m")
        exit(1)
    des = DES(key)
    text = input("[DES]Please Input the Text: ").encode()
    des.keyGen()
    res = des.encrypt(bytes_to_long(text))
    res = long_to_bytes(res).hex()
    print("\033[0;32m[DES]Result(in hex): %s\033[0m" % res)
    exit(0)


def _DES_Decrypt():
    key = input("[DES]Please Input the Key(in hex): ")
    if len(key) != 16:
        print("\033[0;31m[DES]Invalid Key Length\033[0m")
        exit(1)
    try:
        key = int(key, 16)
    except:
        print("\033[0;31m[DES]Invalid Key Format\033[0m")
        exit(1)
    des = DES(key)
    des.keyGen()
    text = input("[DES]Please Input the Text(in hex): ")
    res = des.decrypt(bytes_to_long(bytes.fromhex(text)))
    res = long_to_bytes(res)
    print("\033[0;32m[DES]Result: %s\033[0m" % res)
    exit(0)


def _SM4_Encrypt():
    key = input("[SM4]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[SM4]Invalid Key Length\033[0m")
        exit(1)
    mode = input("[SM4]Please Input the Mode(ECB/CBC/CTR/CFB/OFB): ")
    if mode not in ["ECB", "CBC", "CTR", "CFB", "OFB"]:
        print("\033[0;31m[SM4]Invalid Mode\033[0m")
        exit(1)
    if mode in ["CTR", "CBC", "CFB", "OFB"]:
        iv = input("[SM4]Please Input the IV(in hex): ")
        sm4 = SM4(bytes.fromhex(key), bytes.fromhex(iv))
        if len(iv) != 32:
            print("\033[0;31m[SM4]Invalid IV Length\033[0m")
            exit(1)
    else:
        sm4 = SM4(bytes.fromhex(key))
    func = getattr(sm4, mode+"_encrypt")
    res = func(input("[SM4]Please Input the Text: ").encode()).hex()
    print("\033[0;32m[SM4]Result(in hex): %s\033[0m" % res)
    exit(0)


def _SM4_Decrypt():
    key = input("[SM4]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[SM4]Invalid Key Length\033[0m")
        exit(1)
    mode = input("[SM4]Please Input the Mode(ECB/CBC/CTR/CFB/OFB): ")
    if mode not in ["ECB", "CBC", "CTR", "CFB", "OFB"]:
        print("\033[0;31m[SM4]Invalid Mode\033[0m")
        exit(1)
    if mode in ["CTR", "CBC", "CFB", "OFB"]:
        iv = input("[SM4]Please Input the IV(in hex): ")
        sm4 = SM4(bytes.fromhex(key), bytes.fromhex(iv))
        if len(iv) != 32:
            print("\033[0;31m[SM4]Invalid IV Length\033[0m")
            exit(1)
    else:
        sm4 = SM4(bytes.fromhex(key))
    func = getattr(sm4, mode+"_decrypt")
    res = func(bytes.fromhex(
        input("[SM4]Please Input the Text(in hex): "))).decode()
    print("\033[0;32m[SM4]Result: %s\033[0m" % res)
    exit(0)


def _SM4_Encrypt_File():
    key = input("[SM4]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[SM4]Invalid Key Length\033[0m")
        exit(1)
    mode = input("[SM4]Please Input the Mode(ECB/CBC/CTR/CFB/OFB): ")
    if mode not in ["ECB", "CBC", "CTR", "CFB", "OFB"]:
        print("\033[0;31m[SM4]Invalid Mode\033[0m")
        exit(1)
    if mode in ["CTR", "CBC", "CFB", "OFB"]:
        iv = input("[SM4]Please Input the IV(in hex): ")
        sm4 = SM4(bytes.fromhex(key), bytes.fromhex(iv))
        if len(iv) != 32:
            print("\033[0;31m[SM4]Invalid IV Length\033[0m")
            exit(1)
    else:
        sm4 = SM4(bytes.fromhex(key))
    func = getattr(sm4, mode+"_encrypt")
    try:
        filename = input("[SM4]Please Input the File absolute path: ")
        if not os.path.exists(filename):
            raise FileNotFoundError
        if filename[-4:] == '.bmp':
            plaintext = open(filename, "rb").read()
            header = plaintext[:54]
            data = plaintext[54:]
            data = func(data)
            res = header + data
        else:
            plaintext = open(filename, "rb").read()
            res = func(plaintext)
    except:
        print("\033[0;31m[SM4]File Not Found\033[0m")
        exit(1)
    with open(input("[SM4]Please Input the Output File absolute path: "), "wb") as f:
        f.write(res)
    print("\033[0;32m[SM4]Success\033[0m")
    exit(0)


def _SM4_Decrypt_File():
    key = input("[SM4]Please Input the Key(in hex): ")
    if len(key) != 32:
        print("\033[0;31m[SM4]Invalid Key Length\033[0m")
        exit(1)
    mode = input("[SM4]Please Input the Mode(ECB/CBC/CTR/CFB/OFB): ")
    if mode not in ["ECB", "CBC", "CTR", "CFB", "OFB"]:
        print("\033[0;31m[SM4]Invalid Mode\033[0m")
        exit(1)
    if mode in ["CTR", "CBC", "CFB", "OFB"]:
        iv = input("[SM4]Please Input the IV(in hex): ")
        sm4 = SM4(bytes.fromhex(key), bytes.fromhex(iv))
        if len(iv) != 32:
            print("\033[0;31m[SM4]Invalid IV Length\033[0m")
            exit(1)
    else:
        sm4 = SM4(bytes.fromhex(key))
    func = getattr(sm4, mode+"_decrypt")
    try:
        filename = input("[SM4]Please Input the File absolute path: ")
        if not os.path.exists(filename):
            raise FileNotFoundError
        if filename[-4:] == '.bmp':
            plaintext = open(filename, "rb").read()
            header = plaintext[:54]
            data = plaintext[54:]
            data = func(data)
            res = header + data
        else:
            plaintext = open(filename, "rb").read()
            res = func(plaintext)
    except:
        print("\033[0;31m[SM4]File Not Found\033[0m")
        exit(1)
    with open(input("[SM4]Please Input the Output File absolute path: "), "wb") as f:
        f.write(res)
    print("\033[0;32m[SM4]Success\033[0m")
    exit(0)


def _RSA_Encrypt():
    n = int(input("[RSA]Please Input the n: "))
    e = int(input("[RSA]Please Input the e: "))
    text = input("[RSA]Please Input the Text: ")
    m = bytes_to_long(text.encode())
    c = RSA.encrypt(m, e, n)
    print("\033[0;32m[RSA]Result: %s\033[0m" % str(c))
    exit(0)


def _RSA_Decrypt():
    n = int(input("[RSA]Please Input the n: "))
    d = int(input("[RSA]Please Input the d: "))
    c = int(input("[RSA]Please Input the Ciphertext: "))
    m = RSA.decrypt(c, d, n)
    print("\033[0;32m[RSA]Result: %s\033[0m" % long_to_bytes(m).decode())
    exit(0)


banner = """
\033[0;32m
   _____                  _    __          ___               _ 
  / ____|                | |   \ \        / / |             | |
 | |     _ __ _   _ _ __ | |_ __\ \  /\  / /| |__   ___  ___| |
 | |    | '__| | | | '_ \| __/ _ \ \/  \/ / | '_ \ / _ \/ _ \ |
 | |____| |  | |_| | |_) | || (_) \  /\  /  | | | |  __/  __/ |
  \_____|_|   \__, | .__/ \__\___/ \/  \/   |_| |_|\___|\___|_|
               __/ | |                                         
              |___/|_|                                         
\033[0m
"""
print(banner)

welcome = """
\033[0;35mWelcome to My Crypto Tools, just some useless wheels.
Type `start` for more information.\033[0m
"""
print(welcome)
start()
menu()
choice = get_choice()

table_of_modules = {
    1: _Miller_Rabin_Test,
    2: _Quick_Pow,
    3: _Int2Text,
    4: _Text2Int,
    5: _Inverse,
    6: _SHA1,
    7: _SM3,
    8: _ElGamal,
    9: _AES_Encrypt,
    10: _AES_Decrypt,
    11: _DES_Encrypt,
    12: _DES_Decrypt,
    13: _SM4_Encrypt,
    14: _SM4_Decrypt,
    15: _SM4_Encrypt_File,
    16: _SM4_Decrypt_File,
    17: _RSA_Encrypt,
    18: _RSA_Decrypt
}

table_of_modules[choice]()

#include <iostream>
#include <stdlib.h>
#include <cstring>
#include <cstdint>
#include <iomanip>

using namespace std;

//! First permutation table
const int pc1[56] = {
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4};

//! Second permutauon table
const int pc2[48] = {
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};

//! Initial Permutation table
const int ip[64] = {
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7};

//! inverse Initial Permutation table
const int inv_ip[64] = {
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25};

//! Expand key's table
const int E[48] = {
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1};

//! P Box
const int P_box[32] = {
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25};

//! S Box
const int S_box[8][64] = {
    {14, 0, 4, 15, 13, 7, 1, 4, 2, 14, 15, 2, 11, 13, 8, 1, 3, 10, 10, 6, 6, 12, 12, 11, 5, 9, 9, 5, 0, 3, 7, 8,
     4, 15, 1, 12, 14, 8, 8, 2, 13, 4, 6, 9, 2, 1, 11, 7, 15, 5, 12, 11, 9, 3, 7, 14, 3, 10, 10, 0, 5, 6, 0, 13},
    {15, 3, 1, 13, 8, 4, 14, 7, 6, 15, 11, 2, 3, 8, 4, 14, 9, 12, 7, 0, 2, 1, 13, 10, 12, 6, 0, 9, 5, 11, 10, 5,
     0, 13, 14, 8, 7, 10, 11, 1, 10, 3, 4, 15, 13, 4, 1, 2, 5, 11, 8, 6, 12, 7, 6, 12, 9, 0, 3, 5, 2, 14, 15, 9},
    {10, 13, 0, 7, 9, 0, 14, 9, 6, 3, 3, 4, 15, 6, 5, 10, 1, 2, 13, 8, 12, 5, 7, 14, 11, 12, 4, 11, 2, 15, 8, 1,
     13, 1, 6, 10, 4, 13, 9, 0, 8, 6, 15, 9, 3, 8, 0, 7, 11, 4, 1, 15, 2, 14, 12, 3, 5, 11, 10, 5, 14, 2, 7, 12},
    {7, 13, 13, 8, 14, 11, 3, 5, 0, 6, 6, 15, 9, 0, 10, 3, 1, 4, 2, 7, 8, 2, 5, 12, 11, 1, 12, 10, 4, 14, 15, 9,
     10, 3, 6, 15, 9, 0, 0, 6, 12, 10, 11, 1, 7, 13, 13, 8, 15, 9, 1, 4, 3, 5, 14, 11, 5, 12, 2, 7, 8, 2, 4, 14},
    {2, 14, 12, 11, 4, 2, 1, 12, 7, 4, 10, 7, 11, 13, 6, 1, 8, 5, 5, 0, 3, 15, 15, 10, 13, 3, 0, 9, 14, 8, 9, 6,
     4, 11, 2, 8, 1, 12, 11, 7, 10, 1, 13, 14, 7, 2, 8, 13, 15, 6, 9, 15, 12, 0, 5, 9, 6, 10, 3, 4, 0, 5, 14, 3},
    {12, 10, 1, 15, 10, 4, 15, 2, 9, 7, 2, 12, 6, 9, 8, 5, 0, 6, 13, 1, 3, 13, 4, 14, 14, 0, 7, 11, 5, 3, 11, 8,
     9, 4, 14, 3, 15, 2, 5, 12, 2, 9, 8, 5, 12, 15, 3, 10, 7, 11, 0, 14, 4, 1, 10, 7, 1, 6, 13, 0, 11, 8, 6, 13},
    {4, 13, 11, 0, 2, 11, 14, 7, 15, 4, 0, 9, 8, 1, 13, 10, 3, 14, 12, 3, 9, 5, 7, 12, 5, 2, 10, 15, 6, 8, 1, 6,
     1, 6, 4, 11, 11, 13, 13, 8, 12, 1, 3, 4, 7, 10, 14, 7, 10, 9, 15, 5, 6, 0, 8, 15, 0, 14, 5, 2, 9, 3, 2, 12},
    {13, 1, 2, 15, 8, 13, 4, 8, 6, 10, 15, 3, 11, 7, 1, 4, 10, 12, 9, 5, 3, 6, 14, 11, 5, 0, 0, 14, 12, 9, 7, 2,
     7, 2, 11, 1, 4, 14, 1, 7, 9, 4, 12, 10, 14, 8, 2, 13, 0, 15, 6, 12, 10, 9, 13, 0, 15, 3, 3, 5, 5, 6, 8, 11}};

uint64_t* PC1(uint64_t key)
{
    uint64_t *res = new uint64_t[2];
    for (int i = 0; i < 56; i++)
    {
        int bit_value = (key >> (64 - pc1[i])) & 1;
        if (i < 28)
        {
            res[0] += bit_value << (27 - i);
        }
        else
        {
            res[1] += bit_value << (55 - i);
        }
    }
    return res;
}

uint64_t PC2(uint64_t subkey)
{
    uint64_t res = 0;
    for (int i = 0; i < 48; i++)
    {
        res += ((subkey >> (56 - pc2[i])) & 1) << (47 - i);
    }
    return res;
}

uint64_t leftRotation(uint64_t a, int off)
{
    return (((a & ((1 << (28 - off)) - 1)) << off) + (a >> (28 - off)));
}

void keyGen(uint64_t key, uint64_t *subkeys)
{
    int off[16] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};
    uint64_t *a = PC1(key);
    for (int i = 0; i < 16; i++)
    {
        a[0] = leftRotation(a[0], off[i]);
        a[1] = leftRotation(a[1], off[i]);
        subkeys[i] = PC2((a[0] << 28) + a[1]);
    }
    delete[] a;
}

uint64_t IP(uint64_t text)
{
    uint64_t res = 0;
    for (int i = 0; i < 64; i++)
    {
        res += ((text >> (64 - ip[i])) & 1) << (63 - i);
    }
    return res;
}

uint64_t inv_IP(uint64_t text)
{
    uint64_t res = 0;
    for (int i = 0; i < 64; i++)
    {
        res += ((text >> (64 - inv_ip[i])) & 1) << (63 - i);
    }
    return res;
}

uint64_t Expand(uint64_t text)
{
    uint64_t res = 0;
    for (int i = 0; i < 48; i++)
    {
        res += ((text >> (32 - E[i])) & 1) << (47 - i);
    }
    return res;
}

uint64_t P(uint64_t text)
{
    uint64_t res = 0;
    for (int i = 0; i < 32; i++)
    {
        res += ((text >> (32 - P_box[i])) & 1) << (31 - i);
    }
    return res;
}

uint64_t S(uint64_t text)
{
    uint64_t res = 0;
    for (int i = 7; i >= 0; i--)
    {
        int tmp = text & 0x3f;
        res += S_box[i][tmp] << (4 * (7 - i));
        text >>= 6;
    }
    return res;
}

uint64_t Feistel(uint64_t text, uint64_t subkey)
{
    text = Expand(text);
    uint64_t tmp = text ^ subkey;
    tmp = S(tmp);
    tmp = P(tmp);
    return tmp;
}

void Round(uint64_t *text, uint64_t subkey)
{
    uint64_t tmp = Feistel(text[1], subkey);
    tmp = text[0] ^ tmp;
    text[0] = text[1];
    text[1] = tmp;
}

uint64_t encrypt(uint64_t pt, uint64_t *subkeys)
{
    pt = IP(pt);
    uint64_t res[2] = {0};
    res[0] = 0;
    res[1] = 0;
    res[0] = pt >> 32;
    res[1] = pt & 0xffffffff;

    for (int i = 0; i < 16; i++)
    {
        Round(res, subkeys[i]);
    }
    uint64_t a = inv_IP((res[1] << 32) + res[0]);
    return a;
}

uint64_t decrypt(uint64_t pt, uint64_t *subkeys)
{
    pt = IP(pt);
    uint64_t res[2] = {0};
    res[0] = 0;
    res[1] = 0;
    res[0] = pt >> 32;
    res[1] = pt & 0xffffffff;

    for (int i = 0; i < 16; i++)
    {
        Round(res, subkeys[15-i]);
    }
    uint64_t a = inv_IP((res[1] << 32) + res[0]);
    return a;
}

uint64_t EDE(uint64_t pt, uint64_t *subkeys1, uint64_t *subkeys2)
{
    uint64_t a = encrypt(pt, subkeys1);
    uint64_t b = decrypt(a, subkeys2);
    uint64_t c = encrypt(b, subkeys1);
    return c;
}

int main()
{
    uint64_t iv = 0;
    uint64_t key1 = 0;
    uint64_t key2 = 0;
    int count = 0;
    scanf("%llx", &iv);
    scanf("%llx", &key1);
    scanf("%llx", &key2);
    scanf("%d", &count);
    uint64_t *subkeys1 = new uint64_t[16];
    uint64_t *subkeys2 = new uint64_t[16];
    keyGen(key1, subkeys1);
    keyGen(key2, subkeys2);
    uint64_t *R = new uint64_t[250];
    uint64_t *V = new uint64_t[250];
    for(int i = 0; i<16; i++){
        printf("%llx %llx\n", subkeys1[i], subkeys2[i]);
    }
    for(int i = 0; i<count; i++){
        uint64_t date = 0;
        scanf("%llx", &date);
        if(i == 0){
            uint64_t tmp = EDE(date, subkeys1, subkeys2);
            R[i] = EDE(iv^tmp, subkeys1, subkeys2);
            V[i] = EDE(R[i]^tmp, subkeys1, subkeys2);
        }
        else{
            uint64_t tmp = EDE(date, subkeys1, subkeys2);
            R[i] = EDE(V[i-1]^tmp, subkeys1, subkeys2);
            V[i] = EDE(R[i]^tmp, subkeys1, subkeys2);
        }
    }
    delete[] subkeys1;
    delete[] subkeys2;
    for(int i = 0; i<count; i++){
        std::cout << "0x" << std::setfill('0') << std::setw(16) << std::hex << R[i] << std::endl;
    }
    delete[] R;
    delete[] V;
}
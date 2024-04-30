import math
import random
import struct

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257, 
                     263, 269, 271, 277, 281, 283, 293]

def left_rotate(n, b):
    return ((n << b) | (n >> (32-b))) & 0xFFFFFFFF


def genDegree(n):
    return (random.randrange(2 ** (n - 1) + 1, 2 ** n - 1))


def LowLevel(n):
    f = True
    while f:
        f = False
        num = genDegree(n)
        for i in first_primes_list:
            if num % i == 0:
                f = True
                break
        if not f:
            if primalityTest(num):
                return num
            else:
                f = True


def primalityTest(num):
    k = math.log2(len(str(num)))
    s = 0
    t = num-1
    while t % 2 == 0:
        s += 1
        t //= 2
    for i in range(int(k)):
        a = random.randrange(2, num-2)
        x = pow(a, t, num)
        if x == 1 or x == num - 1:
            continue
        for j in range(s-1):
            x = pow(x, 2, num)
            if x == 1:
                return False
            if x == num - 1:
                break
        else:
            return False
    return True


def hashFunc(m):
    m = bytearray(m, 'utf-8')
    length = len(m) * 8
    m += b'\x80'
    m += b'\x00' * ((56 - len(m) % 64) % 64)
    m += struct.pack(">Q", length)
    for i in range(0, len(m), 64):
        chunk = m[i:i+64]
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack(b'>I', chunk[j * 4: j * 4 + 4])[0]
        for j in range(16, 80):
            w[j] = left_rotate(w[j-3] ^ w[j - 8] ^ w[j-14] ^ w[j-16], 1)
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0
        a, b, c, d, e = h0, h1, h2, h3, h4
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = left_rotate(a, 5) + f + e + k + w[j] & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def numDegreeMod(val, exp, n):
    res, val = 1, val % n
    while exp > 0:
        if exp % 2 == 1:
            res = (res * val) % n
        exp >>= 1
        val = (val**2) % n
    return res


#генерируем параметры домена (p, q, G)
f = True
while f:
    q = LowLevel(160)
    for i in range(4096):
        M = genDegree(1024)
        Mr = M % (2*q)
        p = M - Mr + 1
        if primalityTest(p):
            print("P = ", p)
            print("Q = ", q)
            f = False
            break
#Случайное L
L = random.randrange(1, p - 1)
print("L = ", L)

G = numDegreeMod(L, (p-1)//q, p)
print("G = ", G)

# Генерация ключей
#Cекретный подписывающий ключ 
x = random.randrange(1, q)
print("x = ", x)
# Открытый ключ Y
Y = numDegreeMod(G, x, p)
print("Y = ", Y)

# Подпись сообщения
#Вычисляем значение хэш функции
m = "hello world"
H = hashFunc(m)
print("H = ", H)
#Выбираем случайный эфимерный ключ
k = random.randrange(1, q)
print("k = ", k)

#Вычисляем R и S
R = numDegreeMod(G, k, p) % q
print("R = ", R)
H = int(H, 16)
S = ((H+x*R) * numDegreeMod(k, q-2, q)) % q
print("S = ", S)

A = (H*numDegreeMod(S, q-2, q)) % q
print("A = ", A)
B = (R*numDegreeMod(S, q-2, q)) % q
print("B = ", B)
V = ((numDegreeMod(G, A, p) * numDegreeMod(Y, B, p)) % p) % q
if V == R:
    print("V = R")
    print("V = ", V)
    print("R = ", R)
else:
    print("Подпись не верна")

import math

# Нелинейные функции
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def md5(message):
    # Инициализация переменных
    message = bytearray(message, 'utf-8')
    message_len = len(message) * 8
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += message_len.to_bytes(8, byteorder='little')

    #переменные сцепления
    A = 0x01234567
    B = 0x89abcdef
    C = 0xfedcba98
    D = 0x76543210

    #Константы
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
         0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
         0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
         0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
         0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
         0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
         0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
         0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
         0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
         0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
         0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
         0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
         0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

    


    
    for i in range(0, len(message), 64):
        X = [0] * 16
        for j in range(16):
            X[j] = int.from_bytes(message[i + j * 4:i + j * 4 + 4], byteorder='little')

        AA, BB, CC, DD = A, B, C, D

        # Раунды MD5
        for j in range(64):
            if 0 <= j <= 15:
                g = j
                f = F(B, C, D)
            elif 16 <= j <= 31:
                g = (5 * j + 1) % 16
                f = G(B, C, D)
            elif 32 <= j <= 47:
                g = (3 * j + 5) % 16
                f = H(B, C, D)
            else:
                g = (7 * j) % 16
                f = I(B, C, D)

            temp = D
            D = C
            C = B
            B = B + left_rotate((A + f + K[j] +X[g]) & 0xFFFFFFFF, (math.ceil(j / 16)))
            A = temp

        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF

    hash_result = (A.to_bytes(4, byteorder='little') +
                   B.to_bytes(4, byteorder='little') +
                   C.to_bytes(4, byteorder='little') +
                   D.to_bytes(4, byteorder='little'))

    return ''.join(['{:02x}'.format(i) for i in hash_result])


mess = input('Message for alg: ')
encrypted_string = md5(mess)
print("Encrypted message:", encrypted_string)
import random
import math

# НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Функция для вычисления обратного по модулю
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_rsa_keys(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 2
    while gcd(e, phi_n) != 1:
        e += 1

    d = mod_inverse(e, phi_n)
    return ((e, n), (d, n))

# Шифрование
def encrypt(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

# Дешифрование
def decrypt(encrypted, private_key):
    d, n = private_key
    decrypted = [chr(pow(char, d, n)) for char in encrypted]
    return ''.join(decrypted)




if __name__ == "__main__":
    # Простые числа p и q
    p = 29
    q = 31

    public_key, private_key = generate_rsa_keys(p, q)

    print("Public Key (e, n):", public_key)
    print("Private Key (d, n):", private_key)

    # Сообщение для шифрования
    message = "Hello, this is RSA"

    # Шифрование сообщения
    encrypted_message = encrypt(message, public_key)
    print("Encrypted Message:", encrypted_message)

    # Дешифрование сообщения
    decrypted_message = decrypt(encrypted_message, private_key)
    print("Decrypted Message:", decrypted_message)

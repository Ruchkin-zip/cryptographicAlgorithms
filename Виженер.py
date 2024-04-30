# Создание алфавита 
alphabet = {chr(i+96): i-1 for i in range(1, 27)}

# Ввод сообщения
print("Enter message:")
m = input().lower()

# Ввод ключа
print("\nEnter key:")
k = input().lower()

# Удаление пробелов из сообщения
m = m.replace(" ", "")

# Преобразование сообщения и ключа в списки символов
message = list(m)
key = list(k)
keyOnMessage = message.copy()

# Создание нового списка символов, где каждая буква сообщения заменяется буквой ключа в соответствии с позицией
j = 0
for i in range(0, len(keyOnMessage)):
    keyOnMessage[i] = key[j % len(key)]
    j = j + 1


# Шифрование сообщения с использованием ключа и алфавита
encrypted = message.copy()
for i in range(0, len(message)):
    letter_code = (alphabet[message[i]] + alphabet[keyOnMessage[i]]) % 26
    encrypted_letter = list(filter(lambda x: alphabet[x] == letter_code, alphabet))[0]
    encrypted[i] = encrypted_letter

# Вывод сообщения, ключа и зашифрованного сообщения
print("\nMessage, key and encrypted message:")
print("".join(message))
print("".join(keyOnMessage))
print("".join(encrypted))

# Дешифрование
decrypted = encrypted.copy()
for i in range(0, len(message)):
    letter_code = (alphabet[encrypted[i]] - alphabet[keyOnMessage[i]]) % 26
    decrypted_letter = list(filter(lambda x: alphabet[x] == letter_code, alphabet))[0]
    decrypted[i] = decrypted_letter


print("\nDecrypted message:")
print("".join(decrypted))
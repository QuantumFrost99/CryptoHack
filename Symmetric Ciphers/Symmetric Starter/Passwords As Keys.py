from Crypto.Cipher import AES
import hashlib

ciphertext_hex = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
ciphertext = bytes.fromhex(ciphertext_hex)

with open("text.txt") as f:
    for word in f:
        word = word.strip()
        key = hashlib.md5(word.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        pt = cipher.decrypt(ciphertext)
        if b"crypto{" in pt.lower():
            print("word:", word)
            print("plaintext:", pt)
            break